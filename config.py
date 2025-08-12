import os

class Config:
    SECRET_KEY = 'your-secret-key'  # Used for security (change this to a random string later)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'football.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable unnecessary warnings