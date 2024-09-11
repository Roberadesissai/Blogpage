from app import db
from datetime import datetime


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=True)
    note_id = db.Column(db.Integer, db.ForeignKey("note.id"), nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("comment.id"), nullable=True)

    def __repr__(self):
        return f"Comment('{self.content}', '{self.date_posted}')"
