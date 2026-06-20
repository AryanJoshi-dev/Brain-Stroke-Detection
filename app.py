from flask import Flask, render_template, request, redirect, session
import sqlite3
import numpy as np
import cv2
import os
from tensorflow.keras.models import load_model

app = Flask(__name__)
app.secret_key = "secret_key"

# ---------------------------
# LOAD MODEL (.h5)
# ---------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = load_model(os.path.join(BASE_DIR, "final_model.h5"))

classes = [
    'NORMAL', 'STROKE'
]

# ---------------------------
# DATABASE CONNECTION
# ---------------------------
def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------------------
# CREATE TABLE
# ---------------------------
def create_table():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_table()

# ---------------------------
# HOME PAGE
# ---------------------------
@app.route("/")
def index():
    return render_template("index.html")

# ---------------------------
# REGISTER
# ---------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            conn = get_db()
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            conn.close()

            session["success"] = "Registration Successful! Please login."
            return redirect("/register")   # 🔁 redirect

        except:
            return render_template("register.html", error="Username already exists!")

    # ✅ get message once and remove it
    success = session.pop("success", None)

    return render_template("register.html", success=success)

# ---------------------------
# LOGIN
# ---------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/home")
        else:
            return render_template("login.html", error="Invalid Credentials!")

    return render_template("login.html")

# ---------------------------
# USER HOME
# ---------------------------
@app.route("/home")
def home():
    if "user" in session:
        return render_template("home.html", user=session["user"])
    return redirect("/login")

# ---------------------------
# LOGOUT
# ---------------------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# ---------------------------
# PREDICTION FUNCTION (.h5)
# ---------------------------
@app.route("/prediction", methods=["GET", "POST"])
def prediction():

    if request.method == "POST":

        if "file" not in request.files:
            return "No file uploaded"

        file = request.files["file"]

        if file.filename == "":
            return "No selected file"

        # Read image
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Preprocess
        img = cv2.resize(img, (224, 224))
        img = img / 255.0
        img = np.reshape(img, (1, 224, 224, 3))

        # Prediction
       

        pred = model.predict(img)[0][0]

        print("Prediction value:", pred)

        if pred < 0.5:
            result = "Stroke Detected"
        else:
            result = "Normal"

        print(result)
        print(pred, result)

        return render_template("predictions.html", result=result)

    # 👉 THIS LINE IS IMPORTANT (for GET request)
    return render_template("predictions.html")
# ---------------------------
# RUN APP
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)