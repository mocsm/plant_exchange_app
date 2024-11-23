from app import db
from flask_login import UserMixin

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)

    # Relationship with Plant model
    plants = db.relationship('Plant', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.username}')"

# Plant model
class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)  # Optional image URL
    available_for_exchange = db.Column(db.Boolean, default=True)  # Whether the plant is available for exchange

    # Foreign key for user_id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Plant('{self.name}', '{self.description}')"
