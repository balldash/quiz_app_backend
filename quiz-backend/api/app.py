from flask import Flask
from config import Config
from flask_jwt_extended import JWTManager
from .models import db
from .routes.question import question_bp
from .routes.quiz import quiz_bp

jwt = JWTManager()


def create_app(__name__):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['JWT_SECRET_KEY'] = Config.SECRET_KEY

    jwt.init_app(app)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(question_bp, url_prefix='/api')
    app.register_blueprint(quiz_bp, url_prefix="/api")

    return app
