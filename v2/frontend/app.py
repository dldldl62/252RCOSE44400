from flask import Flask, render_template, request, redirect
import requests
import re

app = Flask(__name__)

BACKEND_URL = "http://backend:5001"

@app.route("/", methods=["GET"])
def index():
    time_message = requests.get(BACKEND_URL + "/api/message").json().get("message", "")
    match = re.search(r'\(updated at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\)', time_message)
    timestamp = match.group(1) if match else None
    message = re.sub(r' \(updated at \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\)', '', time_message) if match else time_message
    return render_template("index.html", current_message=message, timestamp=timestamp)


@app.route("/update", methods=["POST"])
def update():
    new_message = request.form.get("new_message")
    requests.post(BACKEND_URL + "/api/message", json={"message": new_message})
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
