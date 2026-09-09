from flask import request, jsonify
from models import db, SwapRequest, ChatMessage
from flask_jwt_extended import jwt_required, get_jwt_identity

# --- Swap Endpoints ---
def create_swap():
    data = request.json
    swap = SwapRequest(
        requester_id=get_jwt_identity(),
        offered_class_id=data['offered_class_id'],
        desired_class_id=data['desired_class_id']
    )
    db.session.add(swap)
    db.session.commit()
    return jsonify({"message": "Swap request created!"})

def accept_swap(swap_id):
    swap = SwapRequest.query.get(swap_id)
    if swap:
        swap.status = "accepted"
        db.session.commit()
        return jsonify({"message": "Swap accepted!"})
    return jsonify({"error": "Swap not found"}), 404

def get_swaps():
    swaps = SwapRequest.query.filter_by(status="pending").all()
    return jsonify([{
        "id": s.id,
        "offered_class": s.offered_class_id,
        "desired_class": s.desired_class_id
    } for s in swaps])

# --- Chat Endpoints ---
def send_message(swap_id):
    data = request.json
    message = ChatMessage(
        swap_id=swap_id,
        sender_id=get_jwt_identity(),
        receiver_id=data['receiver_id'],
        message_text=data['message_text']
    )
    db.session.add(message)
    db.session.commit()
    return jsonify({"message": "Message sent!"})

def get_messages(swap_id):
    messages = ChatMessage.query.filter_by(swap_id=swap_id).order_by(ChatMessage.timestamp).all()
    return jsonify([{
        "sender_id": m.sender_id,
        "receiver_id": m.receiver_id,
        "text": m.message_text,
        "time": m.timestamp
    } for m in messages])
