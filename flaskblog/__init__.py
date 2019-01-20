from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskblog.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)

    # Loading configuration from config class
    app.config.from_object(Config)

    # Initializing Database
    db.init_app(app)
    # Initialize password encryption
    bcrypt.init_app(app)
    # Initialize login manager
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # Register Routes
    from flaskblog.main.routes import main
    from flaskblog.user.routes import user
    # Register Blueprints
    app.register_blueprint(main)
    app.register_blueprint(user)
    return app
