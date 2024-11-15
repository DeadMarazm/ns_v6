from flask import render_template, redirect, url_for, flash
from flask_security import current_user, login_user, logout_user
from . import admin_bp
from ...forms.forms import LoginForm
from ...models.models import User


@admin_bp.route('/')  # Доступно по /admin/
def admin_home():
    # Если пользователь аутентифицирован и имеет роль admin, перенаправляем в админку
    if current_user.is_authenticated and current_user.has_role('admin'):
        return redirect(url_for('admin.index'))  # Перенаправляем в Flask-Admin dashboard
    return render_template('admin/index.html')  # Иначе выводим страницу входа в админку


@admin_bp.route('/login', methods=['GET', 'POST']) # Доступно по /admin/login
def admin_login():
    if current_user.is_authenticated:
        if current_user.has_role('admin'):
            return redirect(url_for('admin.index'))  # Если пользователь уже залогинен и является админом, то перенаправляем в админку
        else:
            return "Access denied", 403

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            if user.has_role('admin'):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('admin.index'))  #  Перенаправляем на admin.index
            else:
                flash("У вас нет прав для доступа к админке", "danger")
                return redirect(url_for('admin_bp.admin_login'))
        else:
            flash("Неверный email или пароль", "danger")
    return render_template('security/login_admin.html', form=form)


@admin_bp.route('/logout')  # Доступно по /admin/logout
def admin_logout():
    logout_user()
    return redirect(url_for('admin_bp.admin_login'), code=302)
