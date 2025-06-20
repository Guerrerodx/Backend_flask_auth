from flask import Flask
from flasgger import Swagger
from app.routes.auth import auth_bp
from app.routes.users import users_bp

def create_app():
    app = Flask(__name__)
    Swagger(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    return app
