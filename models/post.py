from app import db
from datetime import datetime
from models.tag import post_tags
from models.user import User

post_likes = db.Table('post_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    image_file = db.Column(db.String(20), nullable=True)
    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='dynamic'))
    likes = db.relationship('User', secondary=post_likes, backref=db.backref('posts_liked', lazy='dynamic'))
    liked_by = db.relationship('User', secondary='post_likes', back_populates='liked_posts', lazy='dynamic')
    
    likes = db.relationship('User', secondary='post_likes',
                            backref=db.backref('posts_liked', lazy='dynamic'),
                            lazy='dynamic',
                            overlaps="liked_by,liked_posts")

    @property
    def likes_count(self):
        return self.liked_by.count()

    @property
    def comment_count(self):
        return self.comments.count()

    def is_liked_by(self, user):
        return user in self.likes

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
