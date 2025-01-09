from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .question import Question
from .quiz import Quiz
from .user import User
