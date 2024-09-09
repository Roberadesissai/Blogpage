from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'

    from routes.main import main as main_blueprint
    from routes.auth import auth as auth_blueprint

    # Move this line after importing the blueprints
    csrf.exempt(auth_blueprint)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)