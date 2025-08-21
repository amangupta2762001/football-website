from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import platform

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    if platform.system() == 'Windows':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///football.db'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:////tmp/football.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
    db.init_app(app)
    with app.app_context():
        from . import routes
        routes.init_routes(app)
        db.create_all()
    return app