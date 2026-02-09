import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Cloud Run! System check complete.'

if __name__ == "__main__":
    # Use the PORT environment variable provided by Cloud Run
    # If not found (like on your laptop), default to 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
