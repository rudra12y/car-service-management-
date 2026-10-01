from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Remote requests allow karne ke liye

# AAPKA GOOGLE APPS SCRIPT WEB APP URL YAHAN CHIPKAYEIN:
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwmFGHVj8hgs6lKpKNiTez41vSaqxcZI82-6UCof6pEfezYwToCVdECogMHopy8ii5K/execc"

# Static / Frontend Dashboard Link
SHEET_URL = "https://docs.google.com/spreadsheets/d/1frA1eDY4EMH861I50f8DAlgFghywxoR90dlAjCnUFME/edit"

# Initial Data Storage
bookings = [
    {
        "id": "1",
        "customerName": "Rudra Goswami",
        "phone": "9876543210",
        "carModel": "Activa 6G",
        "serviceType": "Full Service",
        "assignedMechanic": "Ramesh Kumar",
        "status": "In Progress"
    },
    {
        "id": "2",
        "customerName": "dhruvin",
        "phone": "998567461",
        "carModel": "alto",
        "serviceType": "Full Detailing",
        "assignedMechanic": "Not Assigned",
        "status": "Pending"
    },
    {
        "id": "3",
        "customerName": "kartavya",
        "phone": "998565166",
        "carModel": "tigor",
        "serviceType": "Oil Change",
        "assignedMechanic": "Not Assigned",
        "status": "Pending"
    }
]

# -------------------------------------------------------------
# API ROUTES
# -------------------------------------------------------------

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    """Admin Dashboard ke liye saari bookings return karta hai"""
    return jsonify(bookings), 200

@app.route('/api/bookings', methods=['POST'])
def add_booking():
    """Customer Form se nayi booking add karne ke liye"""
    data = request.get_json() or {}
    new_booking = {
        "id": str(len(bookings) + 1),
        "customerName": data.get("customerName", ""),
        "phone": data.get("phone", ""),
        "carModel": data.get("carModel", ""),
        "serviceType": data.get("serviceType", ""),
        "assignedMechanic": data.get("assignedMechanic", "Not Assigned"),
        "status": "Pending"
    }
    bookings.append(new_booking)

    # Automatically send booking data to Google Sheet
    try:
        requests.post(GOOGLE_SCRIPT_URL, json=new_booking, timeout=5)
    except Exception as e:
        print("Google Sheet Sync Error:", e)

    return jsonify({"message": "Booking submitted successfully!", "sheet_url": SHEET_URL, "booking": new_booking}), 201

@app.route('/api/bookings/<booking_id>', methods=['PATCH'])
def update_booking(booking_id):
    """Admin page se Status ya Mechanic update karne ke liye"""
    data = request.get_json() or {}
    for item in bookings:
        if str(item.get("id")) == str(booking_id):
            if "status" in data:
                item["status"] = data["status"]
            if "assignedMechanic" in data:
                item["assignedMechanic"] = data["assignedMechanic"]
            return jsonify({"message": "Updated successfully!", "booking": item}), 200
            
    return jsonify({"error": "Booking not found"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)