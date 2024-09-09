from app import db
from datetime import datetime, timezone
from openai import OpenAI

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    subject = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Float, default=0.0)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    image_file = db.Column(db.String(20), nullable=True)
    comments = db.relationship('Comment', backref='note', lazy='dynamic')

    def __repr__(self):
        return f"Note('{self.title}', '{self.date_posted}')"

    @staticmethod
    def format_with_ai(content, api_key):
        client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")
        
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an AI assistant that helps format and improve study notes. "
                    "Please format the given content into well-structured, easy-to-read study notes."
                ),
            },
            {
                "role": "user",
                "content": content,
            },
        ]

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instruct",
                messages=messages,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in AI formatting: {e}")
            return content  # Return original content if AI formatting fails