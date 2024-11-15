import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Create dummy secret key so we can use sessions
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456790'

    # Create in-memory database
    DATABASE_FILE = 'sample_db.sqlite'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask - Security configuration
    SECURITY_PASSWORD_SALT = 'my_precious_two'  # os.urandom(16).hex()  Генерируем случайную строку
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_REGISTERABLE = True  # Регистрация
    SECURITY_CONFIRMABLE = True  # Подтверждение по email
    SECURITY_RECOVERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False
    SECURITY_SEND_PASSWORD_RESET_NOTICE_TO = ['admin@example.com']  # Список адресов
    SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL = 'admin@example.com'  # Адрес отправителя

    # Flask-Admin configuration
    FLASK_ADMIN = 'admin@example.com'
    FLASK_ADMIN_PASSWORD = 'password'
    FLASK_ADMIN_SWATCH = 'cerulean'
