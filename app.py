from flask import Flask, render_template, request, Response, jsonify, stream_with_context
import sqlite3
from datetime import datetime
import time
import json

from main import comprehensive_response, ONLINE_MODE
from web_search import search_web, fetch_page

app = Flask(__name__)

# =========================
# GLOBAL MODE SWITCH
# =========================
current_mode = {"online": True}  # True = Online, False = Offline

# =========================
# DATABASE CONFIG
# =========================
DB_FILE = "chat_history.db"


def init_db():
    conn = sqlite3.connect("database.db")  # or your db path
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id TEXT,
        role TEXT,
        message TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()


def save_message(chat_id, role, message):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO chats (chat_id, role, message, timestamp)
        VALUES (?, ?, ?, ?)
    """, (chat_id, role, message, datetime.now().isoformat()))

    conn.commit()
    conn.close()


def get_chat_history(chat_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role, message FROM chats
        WHERE chat_id = ?
        ORDER BY id ASC
    """, (chat_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows


# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.json or {}
    user_input = data.get("message", "").strip()
    chat_id = data.get("chat_id", "default")

    # Safety check
    if not user_input:
        return Response("", mimetype="text/event-stream")

    # Save user message immediately
    save_message(chat_id, "user", user_input)

    def generate():
        full_response = ""
        
        # Skip web search by default for speed - users can add "search:" prefix
        web_context = ""
        
        # Only do web search if user explicitly requests it
        if user_input.lower().startswith(("search:", "web:", "current:")):
            try:
                if current_mode["online"]:
                    print("[SEARCHING WEB IN REAL-TIME]")
                    yield f"data: {json.dumps({'type': 'status', 'text': 'Searching web...'})}\n\n"
                    
                    search_query = user_input.split(":", 1)[1].strip()
                    web_sources = search_web(search_query)
                    if web_sources:
                        for src in web_sources[:2]:
                            page = fetch_page(src["url"])
                            if page:
                                web_context += f"\n{page[:500]}\n"
                        
                        yield f"data: {json.dumps({'type': 'status', 'text': 'Processing...'})}\n\n"
            except Exception as e:
                print(f"Web search error: {e}")
                pass

        # Get comprehensive response with web context
        print("[GENERATING RESPONSE]")
        if current_mode["online"]:
            enhanced_input = user_input
            if web_context:
                enhanced_input = f"{user_input}\n\n[Current web information]:{web_context}"
            response_text = comprehensive_response(enhanced_input, mode="online")
        else:
            response_text = comprehensive_response(user_input, mode="offline")

        # Stream response word-by-word with proper formatting
        words = response_text.split()
        for i, word in enumerate(words):
            chunk = word + " "
            full_response += chunk
            
            # Stream as Server-Sent Event
            yield f"data: {json.dumps({'type': 'text', 'text': chunk})}\n\n"
            
            # Add small delay for visual streaming effect
            time.sleep(0.01)

        # Save assistant message AFTER streaming finishes
        save_message(chat_id, "assistant", full_response.strip())
        
        # Send completion signal
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return Response(stream_with_context(generate()), mimetype="text/event-stream")

@app.route("/chats")
def chats():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Get unique chats with their first message as title
    cursor.execute("""
        SELECT chat_id, 
               (SELECT message FROM chats c2 WHERE c2.chat_id = c1.chat_id LIMIT 1) as title
        FROM chats c1
        GROUP BY chat_id
        ORDER BY MAX(id) DESC
    """)
    
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

@app.route("/history/<chat_id>")
def history(chat_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT role, message FROM chats
        WHERE chat_id = ?
        ORDER BY id ASC
    """, (chat_id,))
    
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

@app.route("/mode", methods=["GET", "POST"])
def toggle_mode():
    """Get or toggle the online/offline mode"""
    if request.method == "POST":
        mode = request.json.get("mode", "online")
        current_mode["online"] = (mode == "online")
        return jsonify({"status": "ok", "mode": mode})
    else:
        mode = "online" if current_mode["online"] else "offline"
        return jsonify({"mode": mode})

@app.route("/delete/<chat_id>", methods=["DELETE"])
def delete_chat(chat_id):
    """Delete a specific chat from history"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM chats WHERE chat_id = ?", (chat_id,))
    
    conn.commit()
    conn.close()
    return jsonify({"status": "ok", "message": f"Chat {chat_id} deleted"})

@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store"
    return response

# =========================
# START APP
# =========================
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8080)

