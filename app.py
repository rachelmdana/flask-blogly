"""Blogly application."""

from flask import Flask, redirect, url_for, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
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
    users = User.query.all()
    return render_template('users/list.html', users=users)

@app.route('/tags')
def list_tags():
    tags = Tag.query.all()
    return render_template('tags/list.html', tags=tags)

@app.route('/users/new')
def show_add_user_form():
    return render_template('users/add.html')

@app.route('/users/new', methods=['POST'])
def add_user():
    try:
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        image_url = request.form.get('image_url')

        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url) 

        db.session.add(new_user)
        db.session.commit() 
        return redirect(url_for('show_all_users'))
    
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return render_template('error.html', error_message="An error occurred while adding the user")


@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template ('posts/add.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    try:
        user = User.query.get_or_404(user_id)
        title = request.form.get('title')
        content = request.form.get('content')
        tag_names = request.form.getlist('tags')

        # Create or fetch tags and associate them with the post
        tags = []
        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
            tags.append(tag)

        new_post = Post(title=title, content=content, user=user, tags=tags)

        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('show_user', user_id=user_id))

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error: {str(e)}")

    return render_template('error.html', error_message="An error occurred while adding the post")

@app.route('/users/<int:user_id>/tags/new')
def show_add_tag_form():
    return render_template('tags/add.html')

@app.route('/users/<int:user_id>/tags/new', methods=["POST"])
def add_tag():
    try:
        name = request.form.get('name')
        new_tag = Tag(name=name)
        db.session.add(new_tag)
        db.session.commit()
        return redirect(url_for('list_tags'))
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return render_template('error.html', error_message="An error occurred while adding the tag")

@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    print(user.first_name, user.last_name)
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template('users/detail.html', user=user, posts=posts)

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    return render_template('posts/detail.html', post=post, tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/detail.html', tag=tag)

@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    return redirect(url_for('show_user', user_id=user_id))

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts/edit.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        tag_names = request.form.getlist('tags')

        # Create or fetch tags and associate them with the post
        tags = []
        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
            tags.append(tag)

        post.tags = tags

        db.session.commit()
        return redirect(url_for('show_post', post_id=post_id))

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return render_template('error.html', error_message="An error occurred while editing the post")

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/edit.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    try:
        tag = Tag.query.get_or_404(tag_id)
        tag.name = request.form.get('name')
        db.session.commit()
        return redirect(url_for('list_tags'))
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return render_template('error.html', error_message="An error occurred while editing the tag")

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        posts = Post.query.filter_by(user_id=user_id).all()
        for post in posts:
            db.session.delete(post)
        db.session.delete(user)
        db.session.commit()
        
        return redirect(url_for('show_all_users'))
    
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error: {str(e)}")

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('show_user', user_id=post.user_id))
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error: {str(e)}")

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    try:
        tag = Tag.query.get_or_404(tag_id)
        db.session.delete(tag)
        db.session.commit()
        return redirect(url_for('list_tags'))
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return render_template('error.html', error_message="An error occurred while deleting the tag")