from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskblog.config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)

    # Loading configuration from config class
    app.config.from_object(Config)

    # Initializing Database
    db.init_app(app)

    # Register Routes
    from flaskblog.main.routes import main

    # Register Blueprints
    app.register_blueprint(main)

    return app
