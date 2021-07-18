from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .models import db, User, Task
from todo_app import app
from .login import current_user
from flask import redirect, redirect, url_for

admin = Admin(app, name='TODO APP', template_mode='bootstrap3')


class AuthorizedView(ModelView):
    def is_accessible(self):
        can_access = current_user.is_authenticated and current_user.user_name == 'admin'
        return can_access

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


admin.add_view(AuthorizedView(User, db.session))
admin.add_view(AuthorizedView(Task, db.session))


