from flask import redirect, url_for, request, render_template
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_security import current_user
from app.extensions import admin, db
from app.models.models import User, Role


class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin_bp.admin_login', next=request.url))


class MyAdminIndexView(AdminIndexView):
    @expose('/')  # Удаляем проверку прав доступа, она теперь в SecureModelView
    def index(self):
        # Используем стандартное поведение Flask-Admin
        return super(MyAdminIndexView, self).index()

class UserAdmin(SecureModelView):
    column_list = ('id', 'email', 'active')
    can_edit = True
    can_create = True
    can_delete = False
    can_view_details = True
    column_exclude_list = ['password']
    form_excluded_columns = ['password']

    form_columns = ['username', 'email', 'active']


class RoleAdmin(SecureModelView):
    column_list = ('id', 'name', 'description')
    can_edit = True
    can_delete = False


def init_admin(app):
    admin.init_app(app, index_view=MyAdminIndexView())  # Используем пользовательский класс MyAdminIndexView
    admin.add_view(UserAdmin(User, db.session, name='Users', endpoint='admin_user'))
    admin.add_view(RoleAdmin(Role, db.session, name='Roles', endpoint='admin_role'))

    # Добавляем ссылку на выход
    admin.add_link(MenuLink(name='Выход', endpoint='admin_bp.admin_logout'))
