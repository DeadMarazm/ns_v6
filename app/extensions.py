from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
admin = Admin(name='Админка', template_mode='bootstrap3')
bootstrap = Bootstrap()
bcrypt = Bcrypt()
