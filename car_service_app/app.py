from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Cross-Origin Resource Sharing enable karne ke liye

# Local memory booking list (Server re-start hone par reset hone se bachane ke liye)
bookings = []

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    return jsonify(bookings), 200

@app.route('/api/bookings', methods=['POST'])
def add_booking():
    data = request.json
    if not data or not data.get('customerName') or not data.get('phone'):
        return jsonify({"error": "Invalid data"}), 400
    
    new_booking = {
        "customerName": data.get("customerName"),
        "phone": data.get("phone"),
        "carModel": data.get("carModel"),
        "serviceType": data.get("serviceType"),
        "status": "Pending"
    }
    bookings.append(new_booking)
    return jsonify({"message": "Booking added successfully!"}), 201

@app.route('/api/toggle-status/<int:index>', methods=['POST'])
def toggle_status(index):
    if 0 <= index < len(bookings):
        current_status = bookings[index].get("status", "Pending")
        bookings[index]["status"] = "Completed" if current_status == "Pending" else "Pending"
        return jsonify({"message": "Status updated", "status": bookings[index]["status"]}), 200
    return jsonify({"error": "Index out of range"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)