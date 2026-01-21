print("TEST: Starting minimal Flask")
from flask import Flask

print("TEST: Flask imported")
app = Flask(__name__)

print("TEST: App created")

@app.route('/')
def home():
    return "OK"

print("TEST: Route defined")
print("TEST: About to call app.run()")

try:
    app.run(host='127.0.0.1', port=8080, debug=False, use_reloader=False, threaded=True)
except Exception as e:
    print(f"TEST: Exception: {e}")
    import traceback
    traceback.print_exc()

print("TEST: After app.run()")
