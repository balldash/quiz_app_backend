from . import db


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.String(255), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"),
                        nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'correct_answer': self.correct_answer,
            'quiz_id': self.quiz_id
        }
