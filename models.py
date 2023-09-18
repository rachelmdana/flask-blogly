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

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(200), default='/static/default-profile-image.jpg')

    tags = db.relationship('Tag', secondary='user_tags', back_populates='users')
    posts = db.relationship('Post', backref='user', cascade='all, delete-orphan')

    def __repr__(self):
        """Show info about the user."""
        return f"<User id={self.id} first_name={self.first_name} last_name={self.last_name}>"

class Post(db.Model):
    """Post model."""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    tags = db.relationship('Tag', secondary='post_tags', back_populates='posts')

    def __repr__(self):
        """Show info about the post."""
        return f"<Post id={self.id} title={self.title} created_at={self.created_at}>"

class Tag(db.Model):
    """Tag Model for posts"""
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Define a many-to-many relationship with posts using a secondary table
    posts = db.relationship('Post', secondary='post_tags', back_populates='tags')
    users = db.relationship('User', secondary='user_tags', back_populates='tags')

class PostTag(db.Model):
    '''Join table between Posts and Tags'''
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True, nullable=False)

    # Define relationships between PostTag, Post, and Tag
    post = db.relationship('Post', backref='post_tags')
    tag = db.relationship('Tag', backref='post_tags')

class UserTag(db.Model):
    __tablename__ = 'user_tags'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)