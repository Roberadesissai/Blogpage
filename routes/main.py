from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from models import Post, User, Comment, Tag, Note
from app import db
from forms import PostForm, CommentForm, EditProfileForm, CreateNoteForm, NoteForm
from models import Post
import os
from werkzeug.utils import secure_filename
from flask import current_app
from flask import jsonify, request
from datetime import datetime
import secrets
from PIL import Image

main = Blueprint('main', __name__)


def save_image(form_image):
    if form_image:
        filename = secure_filename(form_image.filename)
        filepath = os.path.join(current_app.root_path, 'static', 'post_images', filename)
        form_image.save(filepath)
        return 'post_images/' + filename
    return None

@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('index.html', posts=posts)

@main.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = Comment(
            content=comment_form.content.data,
            post_id=post.id,
            user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('main.post', post_id=post_id))
    return render_template('post.html', title=post.title, post=post, comment_form=comment_form)

@main.route('/post/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user in post.likes:
        post.likes.remove(current_user)
    else:
        post.likes.append(current_user)
    db.session.commit()
    return jsonify({'likes': len(post.likes), 'liked': current_user in post.likes})

@main.route('/post/<int:post_id>/add_comment', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = Comment(
            content=comment_form.content.data,
            post_id=post.id,
            user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
    return redirect(url_for('main.post', post_id=post_id))

@main.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        image_file = save_image(form.image.data) if form.image.data else None
        post = Post(title=form.title.data, 
                    content=form.content.data, 
                    author=current_user,
                    image_file=image_file)
        new_tags = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
        for tag_name in new_tags:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
            post.tags.append(tag)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.index'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

# @main.route("/post/<int:post_id>/edit", methods=['GET', 'POST'])
# @login_required
# def edit_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
#     form = PostForm()
#     if form.validate_on_submit():
#         post.title = form.title.data
#         post.content = form.content.data
#         if form.image.data:
#             post.image_file = save_image(form.image.data)
#         db.session.commit()
#         flash('Your post has been updated!', 'success')
#         return redirect(url_for('main.post', post_id=post.id))
#     elif request.method == 'GET':
#         form.title.data = post.title
#         form.content.data = post.content
#     return render_template('create_post.html', title='Edit Post', 
#                            form=form, legend='Update Post')


@main.route("/post/<int:post_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        
        # Handle image update if needed
        if form.image.data:
            post.image_file = save_image(form.image.data)

        # Handle tags
        new_tags = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
        # Remove old tags
        post.tags.clear()
        # Add new tags
        for tag_name in new_tags:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
            post.tags.append(tag)

        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.tags.data = ', '.join([tag.name for tag in post.tags])
    return render_template('create_post.html', title='Edit Post', 
                           form=form, legend='Update Post')
# @main.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
# @login_required
# def update_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
#     form = PostForm()
#     if form.validate_on_submit():
#         post.title = form.title.data
#         post.content = form.content.data
#         db.session.commit()
#         flash('Your post has been updated!', 'success')
#         return redirect(url_for('main.post', post_id=post.id))
#     elif request.method == 'GET':
#         form.title.data = post.title
#         form.content.data = post.content
#     return render_template('create_post.html', form=form, legend='Update Post')

# @main.route('/post/<int:post_id>/comment', methods=['POST'])
# @login_required
# def add_comment(post_id):
#     post = Post.query.get_or_404(post_id)
#     form = CommentForm()
#     if form.validate_on_submit():
#         comment = Comment(content=form.content.data, post=post, author=current_user)
#         db.session.add(comment)
#         db.session.commit()
#         flash('Your comment has been added!', 'success')
#     return redirect(url_for('main.post', post_id=post.id))

@main.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.index'))

@main.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

@main.route('/profile')
@login_required
def profile():
    posts_count = current_user.posts.count()
    liked_posts_count = current_user.liked_posts.count()
    comments_count = current_user.comments.count()
    recent_posts = current_user.posts.order_by(Post.date_posted.desc()).limit(6).all()
    return render_template('profile.html', title='Profile',
                           posts_count=posts_count,
                           liked_posts_count=liked_posts_count,
                           comments_count=comments_count,
                           recent_posts=recent_posts,
                           Post=Post) 


@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/notes')
def notes():
    page = request.args.get('page', 1, type=int)
    notes = Note.query.order_by(Note.date_posted.desc()).paginate(page=page, per_page=9)
    return render_template('notes.html', notes=notes)

@main.route('/notes/create', methods=['GET', 'POST'])
@login_required
def create_note():
    form = CreateNoteForm()
    if form.validate_on_submit():
        title = form.title.data
        summary = form.summary.data
        content = form.content.data
        subject = form.subject.data
        image = form.image.data

        # Use AI to format the content
        formatted_content = Note.format_with_ai(content, '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')

        new_note = Note(title=title, summary=summary, content=formatted_content,
                        subject=subject, user_id=current_user.id)

        if image:
            # Save the image and set the image_file attribute
            image_filename = save_image(image)
            new_note.image_file = image_filename

        db.session.add(new_note)
        db.session.commit()
        flash('Your note has been created!', 'success')
        return redirect(url_for('main.notes'))

    return render_template('create_note.html', form=form)

@main.route('/note/<int:note_id>')
def view_note(note_id):
    note = Note.query.get_or_404(note_id)
    return render_template('view_note.html', note=note)

@main.route('/note/edit/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        abort(403)
    form = NoteForm()
    if form.validate_on_submit():
        note.title = form.title.data
        note.summary = form.summary.data
        note.content = form.content.data
        note.subject = form.subject.data
        db.session.commit()
        flash('Your note has been updated!', 'success')
        return redirect(url_for('main.view_note', note_id=note.id))
    elif request.method == 'GET':
        form.title.data = note.title
        form.summary.data = note.summary
        form.content.data = note.content
        form.subject.data = note.subject
    return render_template('edit_note.html', title='Edit Note', form=form, note=note)

@main.route('/note/delete/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    
    # Check if the current user is the author of the note
    if note.user_id != current_user.id:
        abort(403)  # Forbidden access
    
    # Delete the note
    db.session.delete(note)
    db.session.commit()
    
    flash('Your note has been deleted.', 'success')
    return redirect(url_for('main.notes'))

@main.route('/study_groups')
def study_groups():
    return render_template('study_groups.html')

@main.route('/blog')
def blog():
    # Fetch all posts
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    
    # Get the featured post (for example, the most recent post)
    featured_post = Post.query.order_by(Post.date_posted.desc()).first()
    
    return render_template('blog.html', posts=posts, featured_post=featured_post)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static', 'profile_pictures')
    
    # Create the directory if it doesn't exist
    os.makedirs(picture_path, exist_ok=True)
    
    filepath = os.path.join(picture_path, picture_fn)
    
    # Resize the image
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    # Save the picture
    i.save(filepath)
    
    return picture_fn

@main.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.profile_picture.data:
            try:
                picture_file = save_picture(form.profile_picture.data)
                current_user.profile_picture = picture_file
            except Exception as e:
                flash(f'Error updating profile picture: {str(e)}', 'danger')
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        current_user.location = form.location.data
        current_user.website = form.website.data
        
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
        form.location.data = current_user.location
        form.website.data = current_user.website
    
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@main.route('/my-posts')
@login_required
def my_posts():
    posts = Post.query.filter_by(author=current_user).order_by(Post.date_posted.desc()).all()
    return render_template('my_posts.html', posts=posts)

@main.route('/settings')
@login_required
def settings():
    # Add logic for user settings
    return render_template('settings.html')

@main.route('/search')
def search():
    query = request.args.get('q', '')
    filter_type = request.args.get('filter', 'all')

    results = []

    if filter_type in ['all', 'username']:
        users = User.query.filter(User.username.ilike(f'%{query}%')).all()
        results.extend([{'type': 'user', 'username': user.username} for user in users])

    if filter_type in ['all', 'title']:
        posts = Post.query.filter(Post.title.ilike(f'%{query}%')).all()
        results.extend([{'type': 'post', 'id': post.id, 'title': post.title} for post in posts])

    if filter_type in ['all', 'tag']:
        tags = Tag.query.filter(Tag.name.ilike(f'%{query}%')).all()
        results.extend([{'type': 'tag', 'name': tag.name} for tag in tags])

    return jsonify(results)

@main.route('/api/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{'id': post.id, 'title': post.title} for post in posts])