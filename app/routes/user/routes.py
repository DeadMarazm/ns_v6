from flask import render_template, redirect, url_for
from flask_security import login_user, logout_user
from app import db
from app.forms.forms import RegistrationForm, LoginForm
from app.models.models import User
from . import user_bp


@user_bp.route('/')
def index():
    return render_template('index.html')


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('user_bp.index'))
    return render_template('security/login_user.html', form=form)


@user_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user_bp.login'))


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            password=form.password.data,
            fs_uniquifier=form.email.data
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('user_bp.index'))
    return render_template('security/register.html', form=form, title='Register')
