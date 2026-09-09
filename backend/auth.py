from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from models import db, Student

bcrypt = Bcrypt()

def register():
    data = request.json
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    student = Student(name=data['name'], email=data['email'], password=hashed_pw)
    db.session.add(student)
    db.session.commit()
    return jsonify({"message": "Student registered!"})

def login():
    data = request.json
    student = Student.query.filter_by(email=data['email']).first()
    if student and bcrypt.check_password_hash(student.password, data['password']):
        token = create_access_token(identity=student.id)
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401
