from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
      app = Flask(__name__)
      # Use /app/data for SQLite on Render
      app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:////app/data/football.db')
      app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
      app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
      db.init_app(app)
      with app.app_context():
          from . import routes
          routes.init_routes(app)
          # Create data directory for SQLite
          os.makedirs('/app/data', exist_ok=True)
          db.create_all()
      return app