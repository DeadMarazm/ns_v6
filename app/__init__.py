from flask import Flask
from flask_security import SQLAlchemyUserDatastore, Security
from app.extensions import db, migrate, admin, bootstrap
from app.models.models import User, Role
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)
    bootstrap.init_app(app)

    # Настройка Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    # Create the database and the admin user if it doesn't exist
    with app.app_context():
        db.create_all()  # Create database tables
        if not Role.query.filter_by(name='admin').first():
            role = Role(name='admin')
            db.session.add(role)
            db.session.commit()

        if not User.query.filter_by(email='admin@example.com').first():
            admin_user = User(
                fs_uniquifier='admin',
                email='admin@example.com',
                password='password',
                active=True
            )
            admin_user.roles.append(role)
            db.session.add(admin_user)
            db.session.commit()

    # Register blueprints
    from app.routes.user import user_bp
    from app.routes.admin import admin_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')


    return app
