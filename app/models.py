from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    preferences = db.relationship('Preferences', backref='user', lazy=True)

class Preferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
