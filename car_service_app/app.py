@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Poppins', sans-serif;
}

body {
    background-color: #0b0d10;
    color: #ffffff;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
}

.booking-container {
    width: 100%;
    max-width: 500px;
    background: #14171d;
    border: 1px solid #232730;
    border-radius: 12px;
    padding: 30px;
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.6);
}

.brand-header {
    text-align: center;
    margin-bottom: 25px;
}

.brand-header h1 {
    color: #ff5500;
    font-size: 28px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.brand-header p {
    color: #8a94a6;
    font-size: 13px;
    margin-top: 5px;
}

.form-group {
    margin-bottom: 18px;
}

.form-group label {
    display: block;
    font-size: 13px;
    color: #b0b8c5;
    margin-bottom: 6px;
    font-weight: 500;
}

.form-group input,
.form-group select {
    width: 100%;
    padding: 12px 15px;
    background-color: #1a1e26;
    border: 1px solid #2d3340;
    border-radius: 8px;
    color: #ffffff;
    font-size: 14px;
    outline: none;
    transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group select:focus {
    border-color: #ff5500;
}

.form-group input::placeholder {
    color: #5c6575;
}

button#submitBtn {
    width: 100%;
    padding: 14px;
    background-color: #ff5500;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    font-size: 15px;
    font-weight: 600;
    letter-spacing: 1px;
    cursor: pointer;
    text-transform: uppercase;
    transition: background 0.3s ease, transform 0.1s ease;
    margin-top: 10px;
}

button#submitBtn:hover {
    background-color: #e04b00;
}

button#submitBtn:active {
    transform: scale(0.98);
}

button#submitBtn:disabled {
    background-color: #55240c;
    cursor: not-allowed;
}