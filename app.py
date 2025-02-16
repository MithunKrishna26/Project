from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import db, User, Patient, HeartRate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///janitri.db'
db.init_app(app)

# Serve the HTML frontend
@app.route('/')
def index():
    return render_template('index.html')

# User Registration
@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        return "Email and password are required", 400
    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('index'))

# User Login
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        return "Login successful", 200
    else:
        return "Invalid credentials", 401

# Add Patient
@app.route('/patients', methods=['POST'])
def add_patient():
    name = request.form.get('name')
    age = request.form.get('age')
    user_id = request.form.get('user_id')
    if not name or not age or not user_id:
        return "Name, age, and user ID are required", 400
    new_patient = Patient(name=name, age=age, user_id=user_id)
    db.session.add(new_patient)
    db.session.commit()
    return redirect(url_for('index'))

# Get Patient Details
@app.route('/patients', methods=['GET'])
def get_patient():
    patient_id = request.args.get('patient_id')
    patient = Patient.query.get(patient_id)
    if patient:
        return f"Patient Name: {patient.name}, Age: {patient.age}", 200
    else:
        return "Patient not found", 404

# Record Heart Rate
@app.route('/heartrate', methods=['POST'])
def record_heart_rate():
    patient_id = request.form.get('patient_id')
    heart_rate = request.form.get('heart_rate')
    if not patient_id or not heart_rate:
        return "Patient ID and heart rate are required", 400
    new_heart_rate = HeartRate(patient_id=patient_id, heart_rate=heart_rate)
    db.session.add(new_heart_rate)
    db.session.commit()
    return redirect(url_for('index'))

# Get Heart Rate Data
@app.route('/heartrate', methods=['GET'])
def get_heart_rate():
    patient_id = request.args.get('patient_id')
    heart_rates = HeartRate.query.filter_by(patient_id=patient_id).all()
    if heart_rates:
        return "<br>".join([f"Heart Rate: {hr.heart_rate}, Timestamp: {hr.timestamp}" for hr in heart_rates]), 200
    else:
        return "No heart rate data found", 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)