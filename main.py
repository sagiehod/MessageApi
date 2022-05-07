import datetime
import json

from flask import Blueprint, request
from flask_login import login_required, current_user
from models import db, User, Message
from datetime import datetime

main = Blueprint('main', __name__)


@main.route('/send/', methods=['POST'])
@login_required
def send_message():
    to_username = request.args.get("to")
    sbjct = request.json.get("subject")
    msg = request.json.get("message")
    from_user = current_user
    to_user = User.query.filter_by(username=to_username).first()
    if to_user is None:
        return "User not found", 404
    message = Message(
        subject=sbjct, message=msg, sender=from_user.id, receiver=to_user.id, create_date=datetime.now(), unread=True
    )
    db.session.add(message)
    db.session.commit()
    return "Message sent", 200


@main.route('/all-messages/')
@login_required
def get_all_messages():
    to_user = current_user
    #  get all messages from the user or to the user
    messages = Message.query.filter(
        (Message.sender == to_user.id) | (Message.receiver == to_user.id)
    ).all()
    return_messages = list(map(lambda x: x.to_json(), messages))
    if len(return_messages) == 0:
        return "No messages", 200
    return json.dumps(return_messages), 200


@main.route('/unread-messages/')
@login_required
def get_unread_messages():
    to_user = current_user
    messages = Message.query.filter_by(receiver=to_user.id, unread=True).all()
    return_messages = list(map(lambda x: x.to_json(), messages))
    if len(return_messages) == 0:
        return "No messages", 200
    return json.dumps(return_messages), 200


@main.route('/read-message/')
@login_required
def read_message():
    messages = Message.query.filter_by(receiver=current_user.id).all()
    messages_sorted = sorted(messages, key=lambda x: x.create_date, reverse=True)
    if len(messages_sorted) == 0:
        return "No messages", 200
    message_to_read = messages_sorted[0]
    message_to_read.unread = False
    db.session.commit()
    return json.dumps(message_to_read.to_json()), 200


@main.route('/delete-message/')
@login_required
def delete_message():
    message_id = request.args.get("message_id")
    message = Message.query.filter_by(id=message_id).first()
    if message is None:
        return "Message not found", 404
    elif message.sender != current_user.id and message.receiver != current_user.id:
        return "You are not the sender or receiver of this message", 403
    db.session.delete(message)
    db.session.commit()
    return "Message deleted", 200
