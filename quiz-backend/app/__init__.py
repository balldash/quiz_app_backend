from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from app.routes import quiz_routes, auth_routes
        app.register_blueprint(quiz_routes.bp)
        app.register_blueprint(auth_routes.bp)

        db.create_all()

    return app