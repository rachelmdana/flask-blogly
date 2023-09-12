"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect the database to the Flask app."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model."""

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(50),
                           nullable=False)

    last_name = db.Column(db.String(50),
                          nullable=False)

    image_url = db.Column(db.String(200),
                          default='/static/default-profile-image.jpg')

    def __repr__(self):
        """Show info about the user."""
        return f"<User id={self.id} first_name={self.first_name} last_name={self.last_name}>"

class Post(db.Model):
    """Post model."""

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String(100),
                     nullable=False)

    content = db.Column(db.Text,
                       nullable=False)

    created_at = db.Column(db.DateTime,
                           default=datetime.utcnow)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)

    user = db.relationship('User', backref='posts')

    def __repr__(self):
        """Show info about the post."""
        return f"<Post id={self.id} title={self.title} created_at={self.created_at}>"
