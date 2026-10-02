from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Admin Dashboard aur Form requests allow karne ke liye

# Storage (In-memory list)
bookings = [
    {
        "id": "1",
        "customerName": "Rudra Goswami",
        "phone": "9876543210",
        "carModel": "Activa 6G",
        "serviceType": "Full Service",
        "assignedMechanic": "Ramesh Kumar",
        "status": "In Progress"
    }
]

# 1. Admin Panel ke liye saari Bookings Get karna
@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    return jsonify(bookings), 200

# 2. Customer Form se Nayi Booking Receive karna
@app.route('/api/bookings', methods=['POST'])
def add_booking():
    data = request.get_json() or {}
    
    if not data.get("customerName") or not data.get("phone"):
        return jsonify({"error": "Name and Phone are required"}), 400

    new_booking = {
        "id": str(len(bookings) + 1),
        "customerName": data.get("customerName", ""),
        "phone": data.get("phone", ""),
        "carModel": data.get("carModel", ""),
        "serviceType": data.get("serviceType", ""),
        "assignedMechanic": "Not Assigned",
        "status": "Pending"
    }
    bookings.append(new_booking)

    return jsonify({"message": "Booking submitted successfully!", "booking": new_booking}), 201

# 3. Personal Admin Panel se Status update karna
@app.route('/api/bookings/<booking_id>', methods=['PATCH'])
def update_booking(booking_id):
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