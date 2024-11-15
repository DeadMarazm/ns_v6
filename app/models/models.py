from app.extensions import db, bcrypt
from flask_security import UserMixin, RoleMixin

# Таблица связи между пользователями и ролями
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                       )


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, email, password, fs_uniquifier, **kwargs):
        super().__init__(**kwargs)
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.fs_uniquifier = fs_uniquifier
        self.active = True

    def __repr__(self):
        return f'<User {self.username}>'

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
