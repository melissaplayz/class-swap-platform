from flask import request, jsonify
from app import app, db, bcrypt
from models import Student
from flask_jwt_extended import create_access_token

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_student = Student(name=data['name'], email=data['email'], password=hashed_pw)
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    student = Student.query.filter_by(email=data['email']).first()
    if student and bcrypt.check_password_hash(student.password, data['password']):
        token = create_access_token(identity=student.id)
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401

