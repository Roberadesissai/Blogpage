from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, URLField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, Optional, URL
from wtforms.fields import SelectField



class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    tags = StringField('Tags')
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post Comment')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = TextAreaField('Bio', validators=[Length(max=500)])
    profile_picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    location = StringField('Location', validators=[Optional(), Length(max=100)])
    website = StringField('Website', validators=[Optional(), URL()])
    submit = SubmitField('Update Profile')

class CreateNoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    summary = TextAreaField('Summary', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    image = FileField('Image')

class CreateNoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    summary = TextAreaField('Summary', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    subject = SelectField('Subject', choices=[('math', 'Math'), ('science', 'Science'), ('history', 'History'), ('literature', 'Literature'), ('arts', 'Arts'), ('computer_science', 'Computer Science')], validators=[DataRequired()])
    image = FileField('Image')

class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    summary = TextAreaField('Summary', validators=[DataRequired(), Length(min=1, max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    subject = SelectField('Subject', choices=[
        ('math', 'Mathematics'),
        ('science', 'Science'),
        ('literature', 'Literature'),
        ('history', 'History'),
        ('arts', 'Arts'),
        ('computer_science', 'Computer Science')
    ], validators=[DataRequired()])
    submit = SubmitField('Save Changes')