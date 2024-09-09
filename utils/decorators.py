from functools import wraps
from flask import request, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('You need to log in to access this page.')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function