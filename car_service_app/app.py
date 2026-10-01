from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pymysql
import pandas as pd
import io

app = Flask(__name__)
CORS(app)

# MySQL Database Configuration
db_config = {
    'host': '127.0.0.1',
    'port': 3307,
    'user': 'root',
    'password': 'Rudra1',
    'database': 'car_service_db',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    return pymysql.connect(**db_config)

@app.route('/')
def home():
    return jsonify({"message": "Car Service Management API is running!"})

# ==========================================
# 1. USER REGISTER API
# ==========================================
@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')
    role = data.get('role', 'customer')

    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password are required!"}), 400

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                return jsonify({"error": "Email already registered!"}), 400

            sql = "INSERT INTO users (name, email, password, phone, role) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (name, email, password, phone, role))
            connection.commit()
            return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            connection.close()

# ==========================================
# 2. USER LOGIN API
# ==========================================
@app.route('/api/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required!"}), 400

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name, email, password, role FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user and user['password'] == password:
                user.pop('password')
                return jsonify({
                    "message": "Login successful!",
                    "user": user
                }), 200
            else:
                return jsonify({"error": "Invalid email or password!"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            connection.close()

# ==========================================
# 3. BOOK SERVICE API
# ==========================================
@app.route('/api/book-service', methods=['POST'])
def book_service():
    data = request.json
    user_id = data.get('user_id')
    car_model = data.get('car_model')
    service_type = data.get('service_type')
    booking_date = data.get('booking_date')
    notes = data.get('notes', '')

    if not user_id or not car_model or not service_type or not booking_date:
        return jsonify({"error": "user_id, car_model, service_type, and booking_date are required!"}), 400

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO bookings (user_id, car_model, service_type, booking_date, notes, status) 
                VALUES (%s, %s, %s, %s, %s, 'Pending')
            """
            cursor.execute(sql, (user_id, car_model, service_type, booking_date, notes))
            connection.commit()
            return jsonify({"message": "Service booked successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            connection.close()

# ==========================================
# 4. MY BOOKINGS API (GET Endpoint)
# ==========================================
@app.route('/api/my-bookings/<int:user_id>', methods=['GET'])
def get_my_bookings(user_id):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM bookings WHERE user_id = %s ORDER BY created_at DESC"
            cursor.execute(sql, (user_id,))
            bookings = cursor.fetchall()
            return jsonify({"bookings": bookings}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            connection.close()

# ==========================================
# 5. CANCEL BOOKING API
# ==========================================
@app.route('/api/cancel-booking/<int:booking_id>', methods=['PUT'])
def cancel_booking(booking_id):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM bookings WHERE id = %s", (booking_id,))
            if not cursor.fetchone():
                return jsonify({"error": "Booking not found!"}), 404

            sql = "UPDATE bookings SET status = 'Cancelled' WHERE id = %s"
            cursor.execute(sql, (booking_id,))
            connection.commit()
            return jsonify({"message": "Booking cancelled successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            connection.close()

# ==========================================
# 6. ADMIN - GET ALL BOOKINGS API
# ==========================================
@app.route('/api/admin/bookings', methods=['GET'])
def get_all_bookings():
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
                SELECT b.id, u.name as user_name, u.email, u.phone, b.car_model, 
                       b.service_type, b.booking_date, b.status, b.created_at 
                FROM bookings b
                JOIN users u ON b.user_id = u.id
                ORDER BY b.created_at DESC
            """
            cursor.execute(sql)
            bookings = cursor.fetchall()
            return jsonify({"bookings": bookings}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            connection.close()

# ==========================================
# 7. ADMIN - UPDATE BOOKING STATUS API
# ==========================================
@app.route('/api/admin/update-status/<int:booking_id>', methods=['PUT'])
def update_booking_status(booking_id):
    data = request.json
    new_status = data.get('status')

    if not new_status:
        return jsonify({"error": "Status is required!"}), 400

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM bookings WHERE id = %s", (booking_id,))
            if not cursor.fetchone():
                return jsonify({"error": "Booking not found!"}), 404

            sql = "UPDATE bookings SET status = %s WHERE id = %s"
            cursor.execute(sql, (new_status, booking_id))
            connection.commit()
            return jsonify({"message": f"Booking status updated to '{new_status}' successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            connection.close()

# ==========================================
# 8. EXPORT BOOKINGS TO EXCEL API
# ==========================================
@app.route('/api/export-excel', methods=['GET'])
def export_excel():
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
                SELECT b.id, u.name as user_name, u.email, u.phone, b.car_model, 
                       b.service_type, b.booking_date, b.status, b.created_at 
                FROM bookings b
                JOIN users u ON b.user_id = u.id
                ORDER BY b.created_at DESC
            """
            cursor.execute(sql)
            bookings = cursor.fetchall()

            # Convert JSON data to Pandas DataFrame
            df = pd.DataFrame(bookings)

            # Save to memory stream as Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Bookings')
            output.seek(0)

            return send_file(
                output,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name='Car_Service_Bookings.xlsx'
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)