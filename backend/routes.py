from flask import request, jsonify
from app import app, db
from models import Class, SwapRequest
from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/classes', methods=['POST'])
@jwt_required()
def add_class():
    data = request.get_json()
    new_class = Class(
        course_code=data['course_code'],
        class_no=data['class_no'],
        day=data['day'],
        time=data['time'],
        room=data['room']
    )
    db.session.add(new_class)
    db.session.commit()
    return jsonify({"message": "Class added successfully"}), 201

@app.route('/swap', methods=['POST'])
@jwt_required()
def request_swap():
    data = request.get_json()
    requester_id = get_jwt_identity()
    new_swap = SwapRequest(
        requester_id=requester_id,
        target_class_id=data['target_class_id']
    )
    db.session.add(new_swap)
    db.session.commit()
    return jsonify({"message": "Swap request created"}), 201

@app.route('/swap/<int:swap_id>/accept', methods=['POST'])
@jwt_required()
def accept_swap(swap_id):
    swap = SwapRequest.query.get_or_404(swap_id)
    swap.status = "accepted"
    db.session.commit()
    return jsonify({"message": "Swap accepted"}), 200

