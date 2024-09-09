from flask import jsonify
from . import main_bp
from models import Post

@main_bp.route('/api/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{'id': post.id, 'title': post.title} for post in posts])