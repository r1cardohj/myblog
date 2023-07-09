from flask_bootstrap  import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager
from flask_mail import Mail

#template thing init
bootstrap = Bootstrap4()
moment = Moment()

# db init
db = SQLAlchemy()

# login config
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from myblog.models import Admin
    user = Admin.query.get(int(user_id))
    return user

# mail init
mail = Mail()
#


