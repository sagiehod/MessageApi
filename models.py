from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100))
    message = db.Column(db.String(1000))
    sender = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_date = db.Column(db.DateTime)
    unread = db.Column(db.Boolean)

    def to_json(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'message': self.message,
            'sender': User.query.filter_by(id=self.sender).first().username,
            'receiver': User.query.filter_by(id=self.receiver).first().username,
            'date': self.create_date.strftime('%d/%m/%Y %H:%M:%S'),
        }
