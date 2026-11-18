import os

os.makedirs("frontend", exist_ok=True)
os.makedirs("backend", exist_ok=True)

# 1. backend/app.py
with open("backend/app.py", "w", encoding="utf-8") as f:
    f.write("""from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3, os

app = Flask(__name__)
CORS(app)
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
    app.run(host="127.0.0.1", port=5000, debug=True)
""")

# 2. frontend/style.css
with open("frontend/style.css", "w", encoding="utf-8") as f:
    f.write("""@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800;900&family=Montserrat:wght@400;600;700;800&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Montserrat', sans-serif; scroll-behavior: smooth; }
body { background: #050505; color: #fff; overflow-x: hidden; }
h1, h2 { font-family: 'Barlow Condensed', sans-serif; text-transform: uppercase; }
.top-bar { background: #0a0a0a; border-bottom: 1px solid #1c1c1c; padding: 8px 5%; display: flex; justify-content: space-between; align-items: center; font-size: 12px; color: #ccc; }
.yellow-text { color: #f5b800; }
.top-actions { display: flex; align-items: center; gap: 10px; }
.btn-outline-sm { border: 1px solid #444; color: #fff; padding: 4px 12px; border-radius: 4px; text-decoration: none; font-size: 11px; font-weight: 600; }
.btn-yellow-sm { background: #f5b800; color: #000; padding: 5px 14px; border-radius: 4px; text-decoration: none; font-size: 11px; font-weight: 800; }
.navbar { background: rgba(5,5,5,0.96); padding: 14px 5%; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1a1a1a; position: sticky; top: 0; z-index: 1000; }
.logo { font-family: 'Barlow Condensed', sans-serif; font-size: 30px; font-weight: 900; color: #fff; text-decoration: none; }
.logo span { background: #f5b800; color: #000; padding: 0 6px; border-radius: 3px; margin-right: 2px; }
.nav-menu { display: flex; list-style: none; gap: 24px; align-items: center; }
.nav-menu a { color: #e5e5e5; text-decoration: none; font-size: 13px; font-weight: 600; }
.nav-menu a:hover { color: #f5b800; }
.btn-yellow { background: #f5b800; color: #000 !important; padding: 10px 20px; border-radius: 5px; font-weight: 800; font-size: 13px; border: none; cursor: pointer; text-decoration: none; }
.hero-split { display: grid; grid-template-columns: 1.1fr 1fr; align-items: center; min-height: 480px; border-bottom: 1px solid #181818; }
.hero-left { padding: 50px 5% 50px 10%; }
.hero-left h1 { font-size: 52px; font-weight: 900; line-height: 1.05; margin-bottom: 16px; }
.hero-left h1 span { color: #f5b800; }
.hero-left p { color: #ccc; font-size: 15px; line-height: 1.6; margin-bottom: 25px; }
.hero-right { height: 100%; min-height: 480px; }
.hero-right img { width: 100%; height: 100%; object-fit: cover; }
.section-pad { padding: 55px 5%; max-width: 1380px; margin: 0 auto; }
.sec-heading { font-size: 34px; font-weight: 900; margin-bottom: 25px; }
.services-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 18px; }
@media (max-width: 1100px) { .services-grid { grid-template-columns: repeat(3, 1fr); } }
.srv-card { background: #1a1a1a; border: 1px solid #262626; border-radius: 12px; padding: 12px 12px 18px; cursor: pointer; transition: 0.3s; }
.srv-card:hover { background: #f5b800; border-color: #f5b800; transform: translateY(-6px); }
.srv-img-box { width: 100%; height: 210px; border-radius: 8px; overflow: hidden; margin-bottom: 12px; }
.srv-card img { width: 100%; height: 100%; object-fit: cover; }
.srv-title { display: flex; justify-content: space-between; align-items: center; }
.srv-title h4 { font-size: 14px; font-weight: 700; color: #fff; }
.srv-arrow { color: #f5b800; font-size: 18px; font-weight: 800; }
.srv-card:hover h4, .srv-card:hover .srv-arrow { color: #000; }
.stats-social-grid { display: grid; grid-template-columns: 1fr 1.2fr; gap: 25px; }
.stats-boxes { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.stat-card { background: #0f0f0f; border: 1px solid #222; border-radius: 10px; padding: 24px 15px; text-align: center; }
.stat-card h3 { font-size: 36px; color: #f5b800; }
.stat-card p { font-size: 12px; color: #aaa; }
.social-boxes { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.soc-card { border-radius: 10px; padding: 25px 15px; text-align: center; display: flex; flex-direction: column; justify-content: center; }
.soc-yt { background: linear-gradient(135deg, #ff1e1e, #990000); }
.soc-ig { background: linear-gradient(135deg, #f58529, #dd2a7b, #8134af); }
.soc-fb { background: linear-gradient(135deg, #1877f2, #0d47a1); }
.soc-card h3 { font-size: 28px; }
.soc-card p { font-size: 12px; }
.footer { background: #080808; border-top: 1px solid #1c1c1c; padding: 45px 5% 25px; margin-top: 40px; }
.footer-grid { max-width: 1380px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 25px; }
.footer h4 { color: #f5b800; margin-bottom: 12px; }
.footer p, .footer a { color: #999; font-size: 13px; line-height: 1.8; text-decoration: none; display: block; }
.input-dark { width: 100%; background: #141414; border: 1px solid #2a2a2a; padding: 12px 14px; border-radius: 6px; color: #fff; font-size: 13px; margin-bottom: 12px; }
.modal-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.88); justify-content: center; align-items: center; z-index: 2000; padding: 15px; }
.modal-overlay.active { display: flex; }
.cms-box { background: #0d0d0d; border: 1.5px solid #f5b800; border-radius: 10px; padding: 30px; width: 100%; max-width: 420px; position: relative; }
.close-modal { position: absolute; top: 10px; right: 16px; font-size: 26px; color: #888; cursor: pointer; }
""")

# 3. frontend/index.html
with open("frontend/index.html", "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Automotiv Studio Bardoli</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="top-bar">
        <div class="top-contact"><span>✉ rudragoswamiqwe@gmail.com</span><span>📞 7984651607</span></div>
        <div class="top-actions" id="topAuthArea"><a href="login.html" class="btn-yellow-sm">Login / Sign Up</a></div>
    </div>
    <nav class="navbar">
        <a href="index.html" class="logo"><span>AUTO</span>MOTIV</a>
        <ul class="nav-menu">
            <li><a href="index.html">Home</a></li>
            <li><a href="#services">Services</a></li>
            <li><a href="#stats">Stats</a></li>
        </ul>
        <button class="btn-yellow" onclick="openBooking('General Service Enquiry')">Service Enquiry</button>
    </nav>
    <section class="hero-split">
        <div class="hero-left">
            <h1>PAINT PROTECTION.<br><span>DETAILING.</span><br>CUSTOM PAINT JOBS.<br>ALL UNDER ONE ROOF.</h1>
            <p>Automotiv Studio at Damdod Road, Bardoli — Bringing showroom perfection to your vehicle.</p>
            <button class="btn-yellow" onclick="document.getElementById('services').scrollIntoView()">BOOK YOUR SLOT</button>
        </div>
        <div class="hero-right"><img src="https://images.pexels.com/photos/6873088/pexels-photo-6873088.jpeg?auto=compress&cs=tinysrgb&w=1200" alt="Detailing"></div>
    </section>
    <section class="section-pad" id="services">
        <h2 class="sec-heading">CHOOSE FROM A RANGE OF <span class="yellow-text">PREMIUM SERVICES</span></h2>
        <div class="services-grid">
            <div class="srv-card" onclick="openBooking('Paint Protection Film')"><div class="srv-img-box"><img src="https://images.pexels.com/photos/6872148/pexels-photo-6872148.jpeg?auto=compress&cs=tinysrgb&w=600"></div><div class="srv-title"><h4>Paint Protection Film</h4><span class="srv-arrow">↗</span></div></div>
            <div class="srv-card" onclick="openBooking('Ceramic & Graphene Coating')"><div class="srv-img-box"><img src="https://images.pexels.com/photos/6872572/pexels-photo-6872572.jpeg?auto=compress&cs=tinysrgb&w=600"></div><div class="srv-title"><h4>Ceramic & Graphene Coating</h4><span class="srv-arrow">↗</span></div></div>
            <div class="srv-card" onclick="openBooking('Panel Painting')"><div class="srv-img-box"><img src="https://images.pexels.com/photos/8986118/pexels-photo-8986118.jpeg?auto=compress&cs=tinysrgb&w=600"></div><div class="srv-title"><h4>Panel Painting</h4><span class="srv-arrow">↗</span></div></div>
            <div class="srv-card" onclick="openBooking('Full Body Painting')"><div class="srv-img-box"><img src="https://images.pexels.com/photos/8986070/pexels-photo-8986070.jpeg?auto=compress&cs=tinysrgb&w=600"></div><div class="srv-title"><h4>Full Body Painting</h4><span class="srv-arrow">↗</span></div></div>
            <div class="srv-card" onclick="openBooking('Insurance / Accidental Repair')"><div class="srv-img-box"><img src="https://images.pexels.com/photos/4489749/pexels-photo-4489749.jpeg?auto=compress&cs=tinysrgb&w=600"></div><div class="srv-title"><h4>Insurance / Accidental Repair</h4><span class="srv-arrow">↗</span></div></div>
            <div class="srv-card" onclick="openBooking('Sound Damping')"><div class="srv-img-box"><img src="https://images.pexels.com/photos/4489794/pexels-photo-4489794.jpeg?auto=compress&cs=tinysrgb&w=600"></div><div class="srv-title"><h4>Sound Damping</h4><span class="srv-arrow">↗</span></div></div>
            <div class="srv-card" onclick="openBooking('Safety Glazing Film')"><div class="srv-img-box"><img src="https://images.pexels.com/photos/6872601/pexels-photo-6872601.jpeg?auto=compress&cs=tinysrgb&w=600"></div><div class="srv-title"><h4>Safety Glazing Film</h4><span class="srv-arrow">↗</span></div></div>
            <div class="srv-card" onclick="openBooking('Sunroof Protection Film')"><div class="srv-img-box"><img src="https://images.pexels.com/photos/6872164/pexels-photo-6872164.jpeg?auto=compress&cs=tinysrgb&w=600"></div><div class="srv-title"><h4>Sunroof Protection Film</h4><span class="srv-arrow">↗</span></div></div>
            <div class="srv-card" onclick="openBooking('Vinyl Wrap')"><div class="srv-img-box"><img src="https://images.pexels.com/photos/3802510/pexels-photo-3802510.jpeg?auto=compress&cs=tinysrgb&w=600"></div><div class="srv-title"><h4>Vinyl Wrap</h4><span class="srv-arrow">↗</span></div></div>
            <div class="srv-card" onclick="openBooking('Miscellaneous')"><div class="srv-img-box"><img src="https://images.pexels.com/photos/6873088/pexels-photo-6873088.jpeg?auto=compress&cs=tinysrgb&w=600"></div><div class="srv-title"><h4>Miscellaneous</h4><span class="srv-arrow">↗</span></div></div>
        </div>
    </section>
    <section class="section-pad" id="stats" style="padding-top:10px;">
        <div class="stats-social-grid">
            <div class="stats-boxes">
                <div class="stat-card"><h3>1,000+</h3><p>Happy Customers</p></div>
                <div class="stat-card"><h3>20,000+</h3><p>Hours of Work</p></div>
                <div class="stat-card"><h3>2,000+</h3><p>Projects Handled</p></div>
                <div class="stat-card"><h3>8+</h3><p>Years of Experience</p></div>
            </div>
            <div class="social-boxes">
                <div class="soc-card soc-yt"><h3>10,000+</h3><p>YouTube Subscribers</p></div>
                <div class="soc-card soc-ig"><h3>50K+</h3><p>Instagram Followers</p></div>
                <div class="soc-card soc-fb"><h3>30K+</h3><p>Facebook Community</p></div>
            </div>
        </div>
    </section>
    <footer class="footer">
        <div class="footer-grid">
            <div><div class="logo"><span>AUTO</span>MOTIV</div><p>Damdod Road, Bardoli, Gujarat, India.</p></div>
            <div><h4>Quick Links</h4><a href="index.html">Home</a><a href="#services">Services</a><a href="login.html">Login / Admin</a></div>
            <div><h4>Contact Us</h4><p>✉ rudragoswamiqwe@gmail.com</p><p>📞 7984651607</p></div>
        </div>
    </footer>
    <div class="modal-overlay" id="bookingModal">
        <div class="cms-box">
            <span class="close-modal" onclick="closeBooking()">&times;</span>
            <h2 id="modalServiceTitle" style="color:#f5b800; font-size:26px; margin-bottom:15px;">BOOK SERVICE</h2>
            <form id="bookingForm">
                <input type="hidden" id="serviceInput">
                <input type="text" id="custName" class="input-dark" placeholder="Customer Name" required>
                <input type="tel" id="custPhone" class="input-dark" pattern="[0-9]{10}" placeholder="10 Digit Phone" required>
                <input type="text" id="carModel" class="input-dark" placeholder="Car Model (e.g. Creta, Swift)" required>
                <input type="date" id="serviceDate" class="input-dark" required>
                <button type="submit" id="confirmBtn" class="btn-yellow" style="width:100%;">CONFIRM APPOINTMENT</button>
            </form>
        </div>
    </div>
    <script>
        const API_URL = "http://127.0.0.1:5000/api/bookings";
        const currentUser = JSON.parse(localStorage.getItem("studioUser"));
        if (currentUser) {
            document.getElementById("topAuthArea").innerHTML = `<span style="color:#f5b800;font-weight:700;">Hi, ${currentUser.full_name}</span> ${currentUser.role==='admin'?'<a href="admin.html" class="btn-outline-sm">Admin CMS</a>':''} <a href="#" onclick="logout()" class="btn-yellow-sm">Logout</a>`;
        }
        function logout() { localStorage.removeItem("studioUser"); window.location.href = "login.html"; }
        function openBooking(s) {
            if (!currentUser) { alert("Please Login or Sign Up first!"); window.location.href = "login.html"; return; }
            document.getElementById("serviceInput").value = s;
            document.getElementById("modalServiceTitle").innerText = s;
            document.getElementById("custName").value = currentUser.full_name;
            document.getElementById("custPhone").value = currentUser.phone;
            document.getElementById("bookingModal").classList.add("active");
        }
        function closeBooking() { document.getElementById("bookingModal").classList.remove("active"); }
        document.getElementById("bookingForm").addEventListener("submit", async (e) => {
            e.preventDefault();
            const btn = document.getElementById("confirmBtn");
            btn.innerText = "BOOKING..."; btn.disabled = true;
            try {
                const res = await fetch(API_URL, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        customer_name: document.getElementById("custName").value,
                        email: currentUser.email,
                        phone: document.getElementById("custPhone").value,
                        car_model: document.getElementById("carModel").value,
                        service_type: document.getElementById("serviceInput").value,
                        service_date: document.getElementById("serviceDate").value
                    })
                });
                if (res.ok) { alert("Appointment Booked Successfully!"); document.getElementById("bookingForm").reset(); closeBooking(); }
                else { alert("Booking failed."); }
            } catch (err) { alert("Server connection error!"); }
            finally { btn.innerText = "CONFIRM APPOINTMENT"; btn.disabled = false; }
        });
    </script>
</body>
</html>""")

# 4. frontend/login.html
with open("frontend/login.html", "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Automotiv Login</title>
    <link rel="stylesheet" href="style.css">
</head>
<body style="display:flex; flex-direction:column; justify-content:center; align-items:center; min-height:100vh; padding:20px;">
    <a href="index.html" class="logo" style="font-size:38px; margin-bottom:20px;"><span>AUTO</span>MOTIV</a>
    <div class="cms-box">
        <div style="display:flex; border-bottom:1px solid #222; margin-bottom:20px;">
            <div id="tL" onclick="sw('l')" style="flex:1; text-align:center; padding:10px; font-weight:800; color:#f5b800; border-bottom:3px solid #f5b800; cursor:pointer;">LOG IN</div>
            <div id="tS" onclick="sw('s')" style="flex:1; text-align:center; padding:10px; font-weight:800; color:#777; cursor:pointer;">SIGN UP</div>
        </div>
        <form id="lForm">
            <input type="email" id="lEmail" class="input-dark" placeholder="Email Address" required>
            <input type="password" id="lPass" class="input-dark" placeholder="Password" required>
            <button type="submit" id="lBtn" class="btn-yellow" style="width:100%;">Log In</button>
            <p style="font-size:11px; color:#777; text-align:center; margin-top:12px;">Admin: admin@garage.com | admin123</p>
        </form>
        <form id="sForm" style="display:none;">
            <input type="text" id="rName" class="input-dark" placeholder="Full Name" required>
            <input type="email" id="rEmail" class="input-dark" placeholder="Email Address" required>
            <input type="tel" id="rPhone" class="input-dark" pattern="[0-9]{10}" placeholder="10 Digit Mobile" required>
            <input type="password" id="rPass" class="input-dark" placeholder="Password" required>
            <button type="submit" id="sBtn" class="btn-yellow" style="width:100%;">Create Account</button>
        </form>
    </div>
    <a href="index.html" style="color:#888; font-size:12px; margin-top:15px; text-decoration:none;">← Back to Home</a>
    <script>
        const API_BASE = "http://127.0.0.1:5000/api";
        function sw(m) {
            document.getElementById('lForm').style.display = m==='l'?'block':'none';
            document.getElementById('sForm').style.display = m==='s'?'block':'none';
            document.getElementById('tL').style.color = m==='l'?'#f5b800':'#777';
            document.getElementById('tS').style.color = m==='s'?'#f5b800':'#777';
        }
        document.getElementById("sForm").addEventListener("submit", async (e) => {
            e.preventDefault();
            const res = await fetch(`${API_BASE}/signup`, {
                method: "POST", headers: {"Content-Type":"application/json"},
                body: JSON.stringify({ full_name: rName.value, email: rEmail.value, phone: rPhone.value, password: rPass.value })
            });
            const d = await res.json();
            if (res.ok) { alert("Account created! Now Log In."); sw('l'); } else { alert(d.error); }
        });
        document.getElementById("lForm").addEventListener("submit", async (e) => {
            e.preventDefault();
            const res = await fetch(`${API_BASE}/login`, {
                method: "POST", headers: {"Content-Type":"application/json"},
                body: JSON.stringify({ email: lEmail.value, password: lPass.value })
            });
            const d = await res.json();
            if (res.ok) { localStorage.setItem("studioUser", JSON.stringify(d.user)); window.location.href = d.user.role==="admin"?"admin.html":"index.html"; }
            else { alert(d.error); }
        });
    </script>
</body>
</html>""")

# 5. frontend/admin.html
with open("frontend/admin.html", "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin CMS - Automotiv Bardoli</title>
    <link rel="stylesheet" href="style.css">
    <style>
        table { width: 100%; border-collapse: collapse; margin-top: 20px; background: #111; }
        th, td { padding: 14px; border-bottom: 1px solid #222; font-size: 13px; text-align: left; }
        th { background: #1a1a1a; color: #f5b800; }
    </style>
</head>
<body>
    <nav class="navbar">
        <a href="index.html" class="logo"><span>AUTO</span>MOTIV ADMIN</a>
        <div class="top-actions"><a href="index.html" class="btn-outline-sm">Website</a><button onclick="logout()" class="btn-yellow-sm" style="border:none;cursor:pointer;">Logout</button></div>
    </nav>
    <section class="section-pad">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <h2 class="sec-heading">CUSTOMER <span class="yellow-text">BOOKINGS</span></h2>
            <button onclick="load()" class="btn-yellow">Refresh</button>
        </div>
        <div style="overflow-x:auto;">
            <table>
                <thead><tr><th>ID</th><th>Name</th><th>Phone</th><th>Car</th><th>Service</th><th>Date</th><th>Status</th><th>Action</th></tr></thead>
                <tbody id="tb"><tr><td colspan="8">Loading...</td></tr></tbody>
            </table>
        </div>
    </section>
    <script>
        const API_URL = "http://127.0.0.1:5000/api/bookings";
        const u = JSON.parse(localStorage.getItem("studioUser"));
        if (!u || u.role !== "admin") { window.location.href = "login.html"; }
        function logout() { localStorage.removeItem("studioUser"); window.location.href = "login.html"; }
        async function load() {
            const tb = document.getElementById("tb");
            try {
                const res = await fetch(API_URL);
                const data = await res.json();
                tb.innerHTML = data.length ? data.map(b => `<tr>
                    <td>#${b.id}</td><td>${b.customer_name}</td><td>${b.phone}</td><td>${b.car_model}</td>
                    <td style="color:#f5b800;font-weight:700;">${b.service_type}</td><td>${b.service_date}</td><td>${b.status}</td>
                    <td>${b.status==='Pending'?`<button class="btn-yellow-sm" style="border:none;cursor:pointer;" onclick="done(${b.id})">Mark Done</button>`:'✔ Done'}</td>
                </tr>`).join('') : '<tr><td colspan="8">No bookings yet.</td></tr>';
            } catch(e) { tb.innerHTML = '<tr><td colspan="8">Server error. Make sure backend is running.</td></tr>'; }
        }
        async function done(id) {
            await fetch(`${API_URL}/${id}`, { method: "PUT", headers: {"Content-Type":"application/json"}, body: JSON.stringify({status:"Completed"}) });
            load();
        }
        load();
    </script>
</body>
</html>""")

print("LOCAL SETUP COMPLETED SUCCESSFULLY!")