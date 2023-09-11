"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

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
