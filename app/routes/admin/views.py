from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_security import roles_required
from app.extensions import admin, db
from app.forms.forms import RegistrationForm
from app.models.models import User, Role


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    @roles_required('admin')  # Ограничение доступа только для пользователей с ролью 'admin'
    def index(self):
        form = RegistrationForm()  # Create an instance of the form
        return self.render('admin/index.html', form=form)  # Pass the form to the template


class UserView(ModelView):
    column_list = ('id', 'email', 'active')
    can_edit = True
    can_delete = False


class RoleView(ModelView):
    column_list = ('id', 'name', 'description')
    can_edit = True
    can_delete = False


admin.add_view(MyAdminIndexView(name='Admin', endpoint='admin'))
admin.add_view(UserView(User, db.session, 'Users', endpoint='users'))
admin.add_view(RoleView(Role, db.session, 'Roles', endpoint='roles'))
