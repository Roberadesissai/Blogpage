from app import db
from datetime import datetime

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    likes = db.relationship('User', secondary='comment_likes', backref=db.backref('liked_comments', lazy='dynamic'))
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)
    comment_likes = db.Table('comment_likes', db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True), db.Column('comment_id', db.Integer, db.ForeignKey('comment.id'), primary_key=True))

    def __repr__(self):
        return f"Comment('{self.content}', '{self.date_posted}')"