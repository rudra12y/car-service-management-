from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3, os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
DB_PATH = os.path.join(os.path.dirname(__file__), "studio.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, full_name TEXT, email TEXT UNIQUE, phone TEXT, password TEXT, role TEXT DEFAULT 'customer')")
    c.execute("CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY AUTOINCREMENT, customer_name TEXT, email TEXT, phone TEXT, car_model TEXT, service_type TEXT, service_date TEXT, status TEXT DEFAULT 'Pending')")
    c.execute("SELECT * FROM users WHERE email = ?", ("admin@garage.com",))
    if not c.fetchone():
        c.execute("INSERT INTO users (full_name, email, phone, password, role) VALUES (?, ?, ?, ?, ?)", ("Studio Admin", "admin@garage.com", "7984651607", "admin123", "admin"))
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return jsonify({"status": "Automotiv Studio Bardoli Backend Live!"})

@app.route("/api/signup", methods=["POST"])
def signup():
    d = request.json
    try:
        conn = get_db()
        conn.execute("INSERT INTO users (full_name, email, phone, password, role) VALUES (?, ?, ?, ?, 'customer')", (d["full_name"], d["email"], d["phone"], d["password"]))
        conn.commit()
        conn.close()
        return jsonify({"message": "Account created!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists!"}), 400

@app.route("/api/login", methods=["POST"])
def login():
    d = request.json
    conn = get_db()
    u = conn.execute("SELECT * FROM users WHERE email = ? AND password = ?", (d["email"], d["password"])).fetchone()
    conn.close()
    if u:
        return jsonify({"user": dict(u)})
    return jsonify({"error": "Invalid email or password"}), 401

@app.route("/api/bookings", methods=["GET", "POST"])
def bookings():
    conn = get_db()
    if request.method == "POST":
        d = request.json
        conn.execute("INSERT INTO bookings (customer_name, email, phone, car_model, service_type, service_date, status) VALUES (?, ?, ?, ?, ?, ?, 'Pending')", (d["customer_name"], d.get("email", ""), d["phone"], d["car_model"], d["service_type"], d["service_date"]))
        conn.commit()
        conn.close()
        return jsonify({"message": "Booked!"}), 201
    rows = conn.execute("SELECT * FROM bookings ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/bookings/<int:bid>", methods=["PUT"])
def update_booking(bid):
    conn = get_db()
    conn.execute("UPDATE bookings SET status = ? WHERE id = ?", (request.json["status"], bid))
    conn.commit()
    conn.close()
    return jsonify({"message": "Updated"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
