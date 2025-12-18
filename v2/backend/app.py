from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

DATA_PATH = "/data/message.txt"

def read_message():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return f.read()
    return ""

def write_message(msg: str):
    with open(DATA_PATH, "w") as f:
        f.write(msg)


@app.route("/api/message", methods=["GET"])
def get_message():
    message = read_message()
    return jsonify({"message": message})


@app.route("/api/message", methods=["POST"])
def update_message():
    data = request.get_json()
    message = data.get("message")
    time_message = f"{message} (updated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"
    write_message(time_message)
    return jsonify({"status": "ok"})

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
