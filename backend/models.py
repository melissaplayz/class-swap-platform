from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))  # hashed

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20))
    class_no = db.Column(db.String(20))
    day = db.Column(db.String(20))  # Monday–Saturday
    time = db.Column(db.String(50))
    room = db.Column(db.String(50))

class SwapRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    offered_class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    desired_class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    status = db.Column(db.String(20), default="pending")  # pending, accepted, rejected

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    swap_id = db.Column(db.Integer, db.ForeignKey('swap_request.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    message_text = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
