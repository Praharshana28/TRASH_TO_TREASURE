from flask import Flask, render_template, request, jsonify
import json, os

app = Flask(_name_)

USER_FILE = "users.json"

# Ensure users.json exists
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)

def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    users = load_users()

    if username in users:
        return jsonify({"status": "error", "message": "User already exists!"})

    users[username] = {"password": password}
    save_users(users)
    return jsonify({"status": "success", "message": "Signup successful!"})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    users = load_users()

    if username not in users or users[username]["password"] != password:
        return jsonify({"status": "error", "message": "Invalid username or password!"})

    return jsonify({"status": "success", "message": f"Welcome, {username}!"})

if _name_ == "_main_":
    app.run(debug=True)
