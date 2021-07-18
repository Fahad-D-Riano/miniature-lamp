from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from todo_app import app
from.models import User

lm = LoginManager()
lm.init_app(app)

@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)