import base64
from flask import Blueprint, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import Like, Note, Comment, User
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/landing', methods=['GET'])
def landing_page():
    """
    Render the landing page.

    Returns:
        str: Rendered landing page HTML.
    """
    return render_template("landingpage.html", 
            user=current_user if current_user.is_authenticated else None)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """
    Render the home page and handle adding new notes.

    Returns:
        str: Rendered home page HTML.
    """
    if request.method == 'POST': 
        title = request.form.get('title')
        note = request.form.get('note')
        image = request.files.get('image')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        elif not image:
            flash('Please upload an image!', category='error')
        else:
            # Read the image file and encode it as base64
            image_data = base64.b64encode(image.read()).decode('utf-8')
            new_note = Note(title=title, data=note, image_data=image_data, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    """
    Handle deletion of a note.

    Returns:
        str: JSON response indicating success or failure.
    """
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/add-comment', methods=['POST'])
def add_comment():
    """
    Handle adding a comment to a note.

    Returns:
        str: Redirects to blog page with a flash message.
    """
    data = request.form
    note_id = data.get('note_id')
    commenter_name = data.get('commenter_name')
    content = data.get('content')

    if not note_id or not content or not commenter_name:
        flash('Invalid comment data!', 'error')
        return redirect(url_for('views.blog'))

    new_comment = Comment(content=content, commenter_name=commenter_name, note_id=note_id)
    db.session.add(new_comment)
    db.session.commit()

    flash('Comment added successfully!', 'success')
    return redirect(url_for('views.blog'))

@views.route('/delete-comment/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    """
    Handle deletion of a comment.

    Returns:
        str: JSON response indicating success or failure.
    """
    comment = Comment.query.get(comment_id)

    if not comment:
        return jsonify({'error': 'Comment not found!'})

    if comment.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized to delete this comment!'})

    db.session.delete(comment)
    db.session.commit()

    return jsonify({'success': 'Comment deleted successfully!'})
@views.route('/like-comment', methods=['POST'])
def like_comment():
    """
    Handle liking a comment.

    Returns:
        str: JSON response indicating success or failure.
    """
    data = request.form
    comment_id = data.get('comment_id')
    
    if not comment_id:
        return jsonify({'error': 'Invalid comment ID!'})

    comment = Comment.query.get(comment_id)
    
    if not comment:
        return jsonify({'error': 'Comment not found!'})

    like = Like.query.filter_by(comment_id=comment_id, user_id=current_user.id).first()

    if like:
        db.session.delete(like)
        db.session.commit()
        return jsonify({'success': 'Unlike successful!'})

    new_like = Like(comment_id=comment_id, user_id=current_user.id)
    db.session.add(new_like)
    db.session.commit()

    return jsonify({'success': 'Like successful!'})





@views.route('/blog', methods=['GET'])
def blog():
    """
    Render the blog page showing public posts and their associated comments.

    Returns:
        str: Rendered blog page HTML.
    """
    # Fetch public posts
    public_posts = Note.query.all()

    # Fetch authors' names for each post
    authors = {}
    for post in public_posts:
        author = User.query.get(post.user_id)
        authors[post.id] = author.first_name if author else "Unknown"

    return render_template("blog.html", user=current_user, public_posts=public_posts, authors=authors)
