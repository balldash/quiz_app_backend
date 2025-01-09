from . import db


class Quiz(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    questions = db.relationship("Question", backref="quiz", lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'questions': [q.to_dict() for q in self.questions]
        }
