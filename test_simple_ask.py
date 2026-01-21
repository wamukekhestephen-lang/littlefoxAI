#!/usr/bin/env python3
import json
from flask import Flask, Response, request, stream_with_context

app = Flask(__name__)

@app.route("/test_ask", methods=["POST"])
def test_ask():
    try:
        print("STEP 1: Getting request data")
        data = request.json or {}
        user_input = data.get("message", "")
        chat_id = data.get("chat_id", "default")
        
        print(f"STEP 2: Got input: {user_input}, chat_id: {chat_id}")
        
        if not user_input.strip():
            return Response("", mimetype="text/event-stream")
        
        print("STEP 3: Creating generator function")
        
        def generate():
            print("STEP 4: Inside generator")
            yield f"data: {json.dumps({'type': 'status', 'text': 'Testing...'})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
        
        print("STEP 5: Returning Response")
        return Response(stream_with_context(generate()), mimetype="text/event-stream")
    
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True, use_reloader=False)
