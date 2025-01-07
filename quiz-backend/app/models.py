from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    questions = db.relationship("Question", backref="quiz", lazy=True)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.String(255), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)
