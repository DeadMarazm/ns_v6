import logging
from flask import Flask, url_for
from flask_security import SQLAlchemyUserDatastore, Security
from app.extensions import db, migrate, admin, bootstrap, bcrypt
from app.models.models import User, Role
from app.routes.admin.views import init_admin, MyAdminIndexView
from flask_admin import helpers as admin_helpers
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    bcrypt.init_app(app)

    # Настройка Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore, login_url='/admin/login', register_blueprint=False)
    # Local variable'security' value is not used
    @security.context_processor
    def security_context_processor():
        return dict(
            admin_view=admin.index_view,
            theme=admin.theme,
            h=admin_helpers,
            get_url=url_for
        )

    # Создаем database and admin user (из функции)
    create_db_and_admin(app, user_datastore)

    # Регистрация blueprints
    from app.routes.user import user_bp
    from app.routes.admin import admin_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app


def create_db_and_admin(app, user_datastore):
    with app.app_context():
        db.create_all()

        try:
            # Проверка существование роли и пользователя admin
            if not Role.query.filter_by(name='admin').first():
                user_datastore.create_role(name='admin')

            admin_user = User.query.filter_by(email='admin@example.com').first()
            if not admin_user:
                admin_user = user_datastore.create_user(
                    email='admin@example.com',
                    password='password',
                    active=True,
                    fs_uniquifier='admin'
                )
                user_datastore.add_role_to_user(admin_user, 'admin')
                db.session.commit()
            else:
                if not admin_user.has_role('admin'):
                    user_datastore.add_role_to_user(admin_user, 'admin')
                    db.session.commit()
        except Exception as e:
            logging.error(f"Ошибка при создании администратора: {e}")

    # Инициализация admin  интерфейса
    init_admin(app)
