import os
import requests
from dotenv import load_dotenv
import faiss
import numpy as np
import pickle
import fitz  # PyMuPDF
import docx
from web_search import search_web, fetch_page
from ollama_client import ollama_response
from request_classifier import classifier
from knowledge_base import kb
from custom_rules import rules_engine

# =========================
# MODE SWITCH
# =========================
ONLINE_MODE = True   # True = Ollama | False = Offline (FAISS)

# ---------- SETTINGS ----------
DATA_FOLDER = "data"   # folder for your offline files
TEST_URL = "https://www.google.com"  # used to check internet

# Load system prompt from external file
def load_system_prompt(filename="system_prompt.txt"):
    """Load system prompt from external file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Warning: {filename} not found. Using fallback prompt.")
        return "You are a professional-grade intelligent assistant."

SYSTEM_PROMPT = load_system_prompt()

# GREETINGS DATABASE
GREETINGS = {
    "hello": "Hello! How can I assist you today?",
    "hi": "Hi there! What can I help you with?",
    "hey": "Hey! What's on your mind?",
    "good morning": "Good morning! Ready to help. What do you need?",
    "good afternoon": "Good afternoon! How can I help?",
    "good evening": "Good evening! What can I do for you?",
    "how are you": "I'm doing well, thank you for asking! How can I help you?",
    "how's it going": "All good here! What can I help you with?",
    "what's up": "Not much! What can I do for you?",
    "sup": "Hey there! What do you need?",
    "greetings": "Greetings! How can I assist?",
    "welcome": "Thanks for being here! How can I help?",
    "howdy": "Howdy! What brings you here?",
    "bye": "Goodbye! Feel free to come back anytime!",
    "goodbye": "Thanks for chatting! See you soon!",
    "see you": "See you later! Have a great day!",
    "farewell": "Farewell! Come back soon!",
    "thanks": "You're welcome! Happy to help!",
    "thank you": "My pleasure! Anything else I can help with?",
    "appreciate it": "Happy to help! Let me know if you need anything else!",
}
# ------------------------------

load_dotenv()  # loads the .env file

def detect_greeting(user_input):
    """
    Detect if the user input is a greeting.
    Returns the greeting response if detected, None otherwise.
    """
    text = user_input.lower().strip()
    
    # Check for exact or partial matches
    for greeting, response in GREETINGS.items():
        if greeting in text or text in greeting:
            return response
    
    return None

def detect_capabilities_query(user_input):
    """
    Detect if user is asking about AI capabilities.
    Returns the capabilities message if detected, None otherwise.
    """
    text = user_input.lower().strip()
    capability_keywords = ["what can you do", "what are your capabilities", "what can you help with", 
                          "what's your features", "what features do you have", "tell me about yourself",
                          "what can i do with you", "how can you help", "what do you do",
                          "capabilities", "features", "abilities", "what's possible"]
    
    for keyword in capability_keywords:
        if keyword in text:
            return True
    return False

def get_capabilities_response():
    """Return a formatted capabilities message."""
    return """I'm Littlefox AI - a universal intelligent assistant with comprehensive capabilities to handle ANY request:

🔍 **Web Search** - Real-time internet information access
📚 **Local Documents** - Search PDFs, Word docs, text files
💻 **Code Generation** - Write HTML, CSS, JavaScript, Python, React, Vue, etc.
🐛 **Code Debugging** - Debug and optimize any code in any language
🧮 **Mathematics** - Solve equations, derivatives, integrals, limits
📝 **Academic Writing** - Write well-structured essays and research papers
✍️ **Creative Writing** - Generate stories, poems, dialogue, scripts
🎨 **Design & UI** - Suggest layouts, color schemes, design patterns
🌐 **Translation** - Translate between multiple languages
📊 **Analysis** - Compare options, analyze topics, provide pros/cons
🎓 **How-To Guides** - Create step-by-step tutorials and instructions
💬 **General Q&A** - Answer questions on virtually any topic
⚡ **Smart Routing** - Automatically detect and handle your request type
🔗 **Information Synthesis** - Combine data from multiple sources
😊 **Conversation** - Friendly greetings and small talk
⚙️ **Offline Mode** - Work without internet

💻 **PROGRAMMING LANGUAGES**:
HTML, CSS, JavaScript, TypeScript, Python, PHP, Ruby, Go, Rust, Java, C++, C#, Swift, Kotlin, and more!

🎯 **FRAMEWORKS & LIBRARIES**:
React, Vue, Angular, Next.js, Django, Flask, FastAPI, Node.js, Express, Spring, Laravel, and more!

📊 **DATABASES**:
SQL, MongoDB, PostgreSQL, MySQL, Redis, Firebase, DynamoDB, and more!

🚀 **TOOLS & PLATFORMS**:
Docker, Kubernetes, Git, AWS, GCP, Azure, GitHub, GitLab, and more!

✨ **CREATIVE SKILLS**:
UI/UX design, copywriting, content creation, brainstorming, and more!

🌍 **LANGUAGES**:
English, Spanish, French, German, Chinese, Russian, Arabic, Portuguese, Japanese, and more!

HOW TO USE ME:
Just ask for ANYTHING and I'll help:
- "Create a child game in HTML"
- "Debug my Python code"
- "Write an essay about technology"
- "Design a website layout"
- "Translate this to Spanish"
- "Solve this math equation"
- "Create a React component"
- "Analyze pros and cons of AI"
- "How do I learn programming?"

I understand your intent and deliver exactly what you need. No limits - I handle ANY request type!"""

def check_internet():
    """Returns True if internet is available, otherwise False."""
    try:
        requests.get(TEST_URL, timeout=3)
        return True
    except:
        return False
    
def online_browse_response(user_input):
    sources = search_web(user_input)

    if not sources:
        return "I couldn't retrieve live information."

    live_context = ""
    citations = []

    for src in sources:
        page = fetch_page(src["url"])
        if page:
            live_context += page + "\n"
            citations.append(src["url"])

    prompt = f"""
You are answering using LIVE web data fetched in real time.

Content:
{live_context}

Question:
{user_input}

Answer concisely and accurately.
"""

    answer = ollama_response(prompt)

    return answer + "\n\nSources:\n" + "\n".join(citations)


def offline_response(user_input):
    print("\n[OFFLINE MODE - SEMANTIC SEARCH]")
    results = semantic_search(user_input)
    if results:
        for i, res in enumerate(results, 1):
            print(f"\nResult {i}:\n{res[:500]}...\n")
    else:
        print("No relevant information found in local files.")

def comprehensive_response(user_input, mode="online"):
    """
    Universal AI response handler like ChatGPT.
    
    Uses OpenAI API directly for natural, conversational responses to any query.
    
    Args:
        user_input: The user's query
        mode: "online" or "offline" - determines which capabilities to use
    """
    
    # CHECK FOR CAPABILITIES QUERY (only if explicitly asked)
    if detect_capabilities_query(user_input):
        print("\n[CAPABILITIES QUERY]")
        return get_capabilities_response()
    
    print("\n[PROCESSING WITH AI]")
    
    context_sources = []
    combined_context = ""
    
    # Check for special prefixes
    should_search = False
    should_use_kb = False
    domain = None
    
    if user_input.lower().startswith(("search:", "web:", "current:")):
        should_search = True
        user_input = user_input.split(":", 1)[1].strip()
    
    if user_input.lower().startswith("kb:"):
        should_use_kb = True
        user_input = user_input.split(":", 1)[1].strip()
    
    # Check for domain prefix (e.g., "medical: what is...")
    for domain_name in rules_engine.list_domains():
        if user_input.lower().startswith(f"{domain_name}:"):
            domain = domain_name
            user_input = user_input.split(":", 1)[1].strip()
            break
    
    # 1. Use knowledge base if requested
    if should_use_kb:
        try:
            print("  📚 Searching knowledge base...")
            kb_results = kb.search(user_input, top_k=3)
            if kb_results:
                combined_context = "KNOWLEDGE BASE REFERENCES:\n"
                for result in kb_results:
                    combined_context += f"\n{result['text'][:400]}...\n"
        except Exception as e:
            print(f"  Knowledge base search error: {e}")
    
    # 2. Web search if requested
    if should_search and mode == "online":
        try:
            print("  📡 Searching web for current information...")
            web_sources = search_web(user_input)
            if web_sources:
                for src in web_sources[:2]:
                    page = fetch_page(src["url"])
                    if page:
                        combined_context += f"\n[Source: {src['url']}]\n{page[:800]}\n"
                        context_sources.append(src["url"])
        except Exception as e:
            print(f"  Web search unavailable: {e}")
    
    # 3. Build prompt for ChatGPT - with domain context if applicable
    if domain:
        print(f"  ⚙️ Using domain context: {domain}")
        domain_context = rules_engine.get_domain_context(domain)
        system_prompt = domain_context["prompt"] if domain_context else SYSTEM_PROMPT
    else:
        system_prompt = SYSTEM_PROMPT
    
    if combined_context:
        prompt = f"""You are Littlefox AI, a helpful intelligent assistant. Based on the following information, answer the user's question.

REFERENCE INFORMATION:
{combined_context}

USER QUESTION:
{user_input}

Provide a clear, direct answer."""
    else:
        # Default: just answer the question directly
        prompt = user_input
    
    try:
        print("  🤖 Generating response...")
        answer = ollama_response(user_input)
    except Exception as e:
        print(f"  Ollama error: {e}")
        answer = f"Sorry, I'm having trouble processing your request right now. Please try again in a moment."
    
    # Only include sources if user explicitly asked for them
    result = answer
    if any(keyword in user_input.lower() for keyword in ["source", "reference", "cite"]) and context_sources:

        result += "\n\n📌 Sources:\n" + "\n".join(context_sources)
    
    return result

def main():
    print("=== Littlefox AI - Professional Intelligent Assistant ===")
    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break

        task = classify_task(user_input)

        if task == "calculator":
            print(calculator(user_input))
        elif task == "note":
            print(handle_note(user_input))
        elif task == "translate":
            if check_internet():
                print(translate_text(user_input))
            else:
                print("Translation requires internet.")
        elif task == "programming":
            if check_internet():
                print(comprehensive_response(user_input))
            else:
                print(programming_helper(user_input))
        else:  # general chat
            if check_internet():
                print(comprehensive_response(user_input))
            else:
                print(offline_response(user_input))

INDEX_FILE = "faiss_index.pkl"
DOCS_FILE = "docs.pkl"

def build_index():
    documents = []  # store text snippets
    for file in os.listdir(DATA_FOLDER):
        path = os.path.join(DATA_FOLDER, file)
        text = ""
        if file.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        elif file.endswith(".pdf"):
            import fitz
            doc = fitz.open(path)
            for page in doc:
                text += page.get_text()
        elif file.endswith(".docx"):
            import docx
            doc = docx.Document(path)
            text = "\n".join([p.text for p in doc.paragraphs])
        if text.strip():
            documents.append(text)

    # Create embeddings
    embeddings = embed_model.encode(documents, convert_to_numpy=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    # Save index and documents
    faiss.write_index(index, INDEX_FILE)
    with open(DOCS_FILE, "wb") as f:
        pickle.dump(documents, f)
    
    print("Offline semantic index built!")

def load_index():
    index = faiss.read_index(INDEX_FILE)
    with open(DOCS_FILE, "rb") as f:
        documents = pickle.load(f)
    return index, documents

def semantic_search(query, k=3):
    index, documents = load_index()
    query_vec = embed_model.encode([query], convert_to_numpy=True)
    D, I = index.search(query_vec, k)  # distances & indices
    results = [documents[i] for i in I[0]]
    return results


DATA_FOLDER = "data"  # where your files are stored

def search_txt_files(query):
    results = []
    for file in os.listdir(DATA_FOLDER):
        if file.endswith(".txt"):
            with open(os.path.join(DATA_FOLDER, file), "r", encoding="utf-8") as f:
                text = f.read()
                if query.lower() in text.lower():
                    results.append((file, text[:300]))  # preview
    return results

def search_pdf_files(query):
    results = []
    for file in os.listdir(DATA_FOLDER):
        if file.endswith(".pdf"):
            doc = fitz.open(os.path.join(DATA_FOLDER, file))
            text = ""
            for page in doc:
                text += page.get_text()
            if query.lower() in text.lower():
                results.append((file, text[:300]))
    return results

def search_docx_files(query):
    results = []
    for file in os.listdir(DATA_FOLDER):
        if file.endswith(".docx"):
            doc = docx.Document(os.path.join(DATA_FOLDER, file))
            text = "\n".join([p.text for p in doc.paragraphs])
            if query.lower() in text.lower():
                results.append((file, text[:300]))
    return results

def offline_file_search(query):
    results = []
    results.extend(search_txt_files(query))
    results.extend(search_pdf_files(query))
    results.extend(search_docx_files(query))
    return results

def classify_task(user_input):
    text = user_input.lower()
    
    if any(word in text for word in ["calculate", "sum", "subtract", "multiply", "divide"]):
        return "calculator"
    elif any(word in text for word in ["note", "remember", "save"]):
        return "note"
    elif any(word in text for word in ["translate", "translation"]):
        return "translate"
    elif any(word in text for word in ["code", "program", "python", "javascript"]):
        return "programming"
    else:
        return "chat"

def calculator(user_input):
    try:
        # Extract simple math expression from input
        expression = user_input.lower().replace("calculate", "").strip()
        result = eval(expression)  # simple but works for basic math
        return f"The answer is: {result}"
    except Exception as e:
        return "Sorry, I couldn't calculate that."

NOTES_FILE = "notes.txt"

def handle_note(user_input):
    if "save" in user_input.lower() or "remember" in user_input.lower():
        note = user_input.split("note",1)[-1].strip()
        with open(NOTES_FILE, "a", encoding="utf-8") as f:
            f.write(note + "\n")
        return "Note saved!"
    elif "show" in user_input.lower() or "recall" in user_input.lower():
        if not os.path.exists(NOTES_FILE):
            return "No notes found."
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return "Did you want to save or recall a note?"

def translate_text(user_input):
    return ollama_response(user_input)

def programming_helper(user_input):
    results = offline_file_search(user_input)  # search your programming notes
    if results:
        return f"Found in your notes:\n{results[0][1]}"
    else:
        return "No programming info found locally. Try online mode."

if __name__ == "__main__":
    # create data folder if missing
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    main()

