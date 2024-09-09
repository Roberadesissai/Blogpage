from app import db
from app import db
from datetime import datetime
from models.tag import post_tags

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
    # Remove the 'likes' relationship from here
    image_file = db.Column(db.String(20), nullable=True)
    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='dynamic'))
    

    @property
    def likes_count(self):
        return self.liked_by.count()

    @property
    def comment_count(self):
        return self.comments.count()
    
    @property
    def like_count(self):
        return self.likes.count()
    
    def is_liked_by(self, user):
        return user in self.likes

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"