import os


class Config:
    SECRET_KEY = 'WEedr2KEnQxtYYWnDOnKjq5846dTQfwE'

    # Creating absolute path to config file
    db_path = os.path.join(os.path.dirname('config.py'), 'site.db')
    db_uri = 'sqlite:///{}'.format(db_path)
    SQLALCHEMY_DATABASE_URI = db_uri

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
