from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, URLField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, Optional, URL
from wtforms.fields import SelectField, IntegerField
from wtforms.validators import ValidationError
from models.user import User




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
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    school = StringField('School', validators=[DataRequired()])
    major = StringField('Major', validators=[DataRequired()])
    year = SelectField('Year', choices=[
        ('Freshman', 'Freshman'),
        ('Sophomore', 'Sophomore'),
        ('Junior', 'Junior'),
        ('Senior', 'Senior'),
        ('Graduate', 'Graduate')
    ], validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValidationError('That username is taken. Please choose a different one.')

    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError('That email is taken. Please choose a different one.')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValidationError('That username is taken. Please choose a different one.')

    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError('That email is taken. Please choose a different one.')
    #     if not email.data.endswith('.edu'):
    #         raise ValidationError('Please use a valid .edu email address.')

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