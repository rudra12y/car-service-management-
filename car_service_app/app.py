from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

bookings = []

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    return jsonify(bookings), 200

@app.route('/api/bookings', methods=['POST'])
def add_booking():
    data = request.json
    if not data or not data.get('customerName') or not data.get('phone'):
        return jsonify({"error": "Invalid data"}), 400
    
    selected_date = data.get("bookingDate")
    
    # 1 Date par kitni bookings hain check karein
    existing_count = sum(1 for b in bookings if b.get("bookingDate") == selected_date)
    
    # 3 car limit cross hote hi 'Waiting' assign karein
    booking_status = "Waiting" if existing_count >= 3 else "Pending"

    new_booking = {
        "customerName": data.get("customerName"),
        "phone": data.get("phone"),
        "carModel": data.get("carModel"),
        "bookingDate": selected_date,
        "serviceType": data.get("serviceType"),
        "status": booking_status
    }
    bookings.append(new_booking)
    
    return jsonify({
        "message": "Booking added successfully!",
        "status": booking_status
    }), 201

@app.route('/api/toggle-status/<int:index>', methods=['POST'])
def toggle_status(index):
    if 0 <= index < len(bookings):
        current_status = bookings[index].get("status", "Pending")
        if current_status == "Completed":
            bookings[index]["status"] = "Pending"
        else:
            bookings[index]["status"] = "Completed"
            
        return jsonify({"message": "Status updated", "status": bookings[index]["status"]}), 200
    return jsonify({"error": "Index out of range"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    