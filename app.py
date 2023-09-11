"""Blogly application."""

from flask import Flask, redirect, url_for, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# Configure Flask Debug Toolbar
app.config['SECRET_KEY'] = 'millieban'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)


connect_db(app)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def index():
    return redirect(url_for('show_all_users'))

@app.route('/users')
def show_all_users():
    # Fetch all users from the database
    users = User.query.all()
    return render_template('users/list.html', users=users)

@app.route('/users/new')
def show_add_user_form():
    return render_template('users/add.html')

@app.route('/users/new', methods=['POST'])
def add_user():
    try:
        # Process the form data and create a new user
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        image_url = request.form.get('image_url')  # Retrieve the image URL
        
        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)  # Include image_url
        
        db.session.add(new_user)  # Add the new user to the session
        db.session.commit()  # Commit the transaction to save the new user
        
        return redirect(url_for('show_all_users'))
    except SQLAlchemyError as e:
        # Handle the error, log it, and possibly rollback the transaction
        db.session.rollback()
        print(f"Error: {str(e)}")

@app.route('/users/<int:user_id>')
def show_user(user_id):
    # Fetch the user by user_id from the database
    user = User.query.get_or_404(user_id)
    return render_template('users/detail.html', user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    # Fetch the user by user_id from the database
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    # Process the form data and update the user in the database
    # Redirect to the user's detail page after editing
    return redirect(url_for('show_user', user_id=user_id))

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    # Delete the user by user_id from the database
    # Redirect to the list of users after deletion
    return redirect(url_for('show_all_users'))
