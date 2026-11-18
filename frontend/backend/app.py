from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_NAME = "car_service.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Users Table (Sign Up & Login mate)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'customer'
        )
    ''')
    # Bookings Table
    cursor.execute('''
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
    ''')
    # Default Admin Account
    cursor.execute("SELECT * FROM users WHERE email = 'admin@garage.com'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (full_name, email, phone, password, role) VALUES (?, ?, ?, ?, ?)",
            ("Studio Admin", "admin@garage.com", "9999999999", "admin123", "admin")
        )
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Car Service Studio Backend is Live!"})

# 1. SIGN UP API
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (full_name, email, phone, password) VALUES (?, ?, ?, ?)",
            (data["full_name"], data["email"], data["phone"], data["password"])
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Account created successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already registered! Please login."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2. LOGIN API
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, full_name, email, phone, role FROM users WHERE email = ? AND password = ?",
        (data["email"], data["password"])
    )
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({
            "message": "Login successful!",
            "user": {
                "id": user[0],
                "full_name": user[1],
                "email": user[2],
                "phone": user[3],
                "role": user[4]
            }
        }), 200
    return jsonify({"error": "Invalid email or password"}), 401

# 3. CREATE BOOKING API
@app.route("/api/bookings", methods=["POST"])
def create_booking():
    data = request.json
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO bookings (customer_name, email, phone, car_model, service_type, service_date) VALUES (?, ?, ?, ?, ?, ?)",
            (
                data["customer_name"],
                data.get("email", ""),
                data["phone"],
                data["car_model"],
                data["service_type"],
                data["service_date"]
            )
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Booking confirmed!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 4. GET BOOKINGS API (Admin mate badha, Customer mate potana)
@app.route("/api/bookings", methods=["GET"])
def get_bookings():
    email = request.args.get("email")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if email:
        cursor.execute("SELECT * FROM bookings WHERE email = ? ORDER BY id DESC", (email,))
    else:
        cursor.execute("SELECT * FROM bookings ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    bookings = []
    for r in rows:
        bookings.append({
            "id": r[0],
            "customer_name": r[1],
            "email": r[2],
            "phone": r[3],
            "car_model": r[4],
            "service_type": r[5],
            "service_date": r[6],
            "status": r[7]
        })
    return jsonify(bookings), 200

# 5. UPDATE BOOKING STATUS API (Admin mate)
@app.route("/api/bookings/<int:booking_id>", methods=["PUT"])
def update_booking(booking_id):
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE bookings SET status = ? WHERE id = ?", (data["status"], booking_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Status updated!"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)