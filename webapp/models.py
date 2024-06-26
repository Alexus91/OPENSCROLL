from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    """Represents a note in the application."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))  
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    image_data = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='note', lazy=True)


class User(db.Model, UserMixin):
    """Represents a user in the application."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    avatar_url = db.Column(db.String(255))  
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note', backref='user', lazy=True)

class Comment(db.Model):
    """Represents a comment on a note in the application."""

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    commenter_name = db.Column(db.String(150))
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))

