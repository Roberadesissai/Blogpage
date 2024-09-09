from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    liked_posts = db.relationship('Post', secondary='post_likes', backref=db.backref('liked_by', lazy='dynamic'), lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    bio = db.Column(db.Text)
    location = db.Column(db.String(100))
    website = db.Column(db.String(200))
    notes = db.relationship('Note', backref='author', lazy='dynamic')


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))