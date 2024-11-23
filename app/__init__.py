from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Make sure to use a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Database URI for SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to the login page if not authenticated

# User loader function for Flask-Login
from app.models import User  # Import the User model
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Load user from database based on user_id

# Import routes after db initialization
from app import routes

# Create all tables if they don't exist
with app.app_context():
    db.create_all()
