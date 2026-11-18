from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

DB_PATH = os.path.join(os.path.dirname(__file__), "studio.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'customer'
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            email TEXT,
            phone TEXT NOT NULL,
            car_model TEXT NOT NULL,
            service_type TEXT NOT NULL,
            service_date TEXT NOT NULL,
            status TEXT DEFAULT 'Pending'
        )
    """)
    # Default Admin Account
    cursor.execute("SELECT * FROM users WHERE email = ?", ("admin@garage.com",))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (full_name, email, phone, password, role) VALUES (?, ?, ?, ?, ?)",
            ("Studio Admin", "admin@garage.com", "7984651607", "admin123", "admin")
        )
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Automotiv Studio Bardoli Backend is Live!"})

@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json
    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO users (full_name, email, phone, password, role) VALUES (?, ?, ?, ?, 'customer')",
            (data["full_name"], data["email"], data["phone"], data["password"])
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Account created successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already registered!"}), 400

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ? AND password = ?",
        (data["email"], data["password"])
    ).fetchone()
    conn.close()
    if user:
        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "full_name": user["full_name"],
                "email": user["email"],
                "phone": user["phone"],
                "role": user["role"]
            }
        })
    return jsonify({"error": "Invalid email or password"}), 401

@app.route("/api/bookings", methods=["GET", "POST"])
def handle_bookings():
    conn = get_db()
    if request.method == "POST":
        data = request.json
        conn.execute(
            "INSERT INTO bookings (customer_name, email, phone, car_model, service_type, service_date, status) VALUES (?, ?, ?, ?, ?, ?, 'Pending')",
            (data["customer_name"], data.get("email", ""), data["phone"], data["car_model"], data["service_type"], data["service_date"])
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Booking confirmed!"}), 201

    rows = conn.execute("SELECT * FROM bookings ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route("/api/bookings/<int:booking_id>", methods=["PUT"])
def update_booking(booking_id):
    data = request.json
    conn = get_db()
    conn.execute("UPDATE bookings SET status = ? WHERE id = ?", (data["status"], booking_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Status updated"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)