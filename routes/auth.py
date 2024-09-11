from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from app import db
import bcrypt
from sqlalchemy.exc import IntegrityError
from forms import RegistrationForm
import re
from urllib.parse import urlparse
from flask import request, url_for, redirect, session
from flask_login import current_user, login_user


auth = Blueprint('auth', __name__)





@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        session['just_logged_in'] = True
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if username is provided
        if not username:
            return render_template('login.html') + '''
                <script>
                    showFlashMessage('Please enter a username.', 'red', 'Error');
                </script>
            '''

        # Check if password is provided
        if not password:
            return render_template('login.html') + '''
                <script>
                    showFlashMessage('Please enter a password.', 'red', 'Error');
                </script>
            '''

        user = User.query.filter_by(username=username).first()
        
        if not user:
            return render_template('login.html') + '''
                <script>
                    showFlashMessage('No account found with this username.', 'red', 'Error');
                </script>
            '''
        
        if not user.check_password(password):
            return render_template('login.html') + '''
                <script>
                    showFlashMessage('Incorrect password. Please try again.', 'red', 'Error');
                </script>
            '''
        
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.dashboard')
        return redirect(next_page)
    
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.dashboard'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check username length
        if len(form.username.data) < 4:
            return render_template('register.html', form=form) + '''
                <script>
                    showFlashMessage('Username must be at least 4 characters long.', 'red', 'Error');
                </script>
            '''

        # Check if username already exists
        if User.query.filter_by(username=form.username.data).first():
            return render_template('register.html', form=form) + '''
                <script>
                    showFlashMessage('This username is already taken.', 'red', 'Error');
                </script>
            '''

        # Check if email is .edu
        if not form.email.data.lower().endswith('.edu'):
            return render_template('register.html', form=form) + '''
                <script>
                    showFlashMessage('Please use a valid .edu email address.', 'red', 'Error');
                </script>
            '''

        # Check if email already exists
        if User.query.filter_by(email=form.email.data).first():
            return render_template('register.html', form=form) + '''
                <script>
                    showFlashMessage('This email is already registered.', 'red', 'Error');
                </script>
            '''

        # Check password length
        if len(form.password.data) < 8:
            return render_template('register.html', form=form) + '''
                <script>
                    showFlashMessage('Password must be at least 8 characters long.', 'red', 'Error');
                </script>
            '''

        # Check password complexity
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', form.password.data):
            return render_template('register.html', form=form) + '''
                <script>
                    showFlashMessage('Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character.', 'red', 'Error');
                </script>
            '''

        # Check password match
        if form.password.data != form.confirm_password.data:
            return render_template('register.html', form=form) + '''
                <script>
                    showFlashMessage('Passwords do not match.', 'red', 'Error');
                </script>
            '''

        # Check if school is provided
        if not form.school.data:
            return render_template('register.html', form=form) + '''
                <script>
                    showFlashMessage('Please provide your school name.', 'red', 'Error');
                </script>
            '''

        # Check if major is provided
        if not form.major.data:
            return render_template('register.html', form=form) + '''
                <script>
                    showFlashMessage('Please provide your major.', 'red', 'Error');
                </script>
            '''

        # If all checks pass, create new user
        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            school=form.school.data,
            major=form.major.data,
            year=form.year.data  # No need to convert to int
        )
        new_user.set_password(form.password.data)

        try:
                db.session.add(new_user)
                db.session.commit()
               
                return redirect(url_for('auth.login'))
        except Exception as e:
                db.session.rollback()
                
                return render_template('register.html', form=form)

                # If form validation fails, show the first error
    if form.errors:
                first_error = next(iter(form.errors.values()))[0]
                flash(first_error, 'error')

    return render_template('register.html', form=form)

