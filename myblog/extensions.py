from flask_bootstrap  import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask import current_app
from flask_wtf import CSRFProtect

#template thing init
bootstrap = Bootstrap4()
moment = Moment()

# db init
db = SQLAlchemy()
migrate = Migrate()

# login config
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from myblog.models import Admin
    user = Admin.query.get(int(user_id))
    return user

login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'
login_manager.login_message = u'请先登录'

# mail init
mail = Mail()
# safe init
csrf = CSRFProtect()


