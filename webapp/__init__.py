from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    """
    Create and configure the Flask application instance.

    Returns:
        Flask: An instance of the Flask application.
    """
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'Alexus91'

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    from .view import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    with app.app_context():
        db.create_all()
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        """
        Load a user by their ID for Flask-Login.

        Args:
            id (int): The ID of the user.

        Returns:
            User: The User object corresponding to the provided ID.
        """
        return User.query.get(int(id))

    return app

def create_database(app):
    """
    Create the database if it does not exist.

    Args:
        app (Flask): The Flask application instance.
    """
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
