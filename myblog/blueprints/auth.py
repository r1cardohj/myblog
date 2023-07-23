from flask import Blueprint,redirect,url_for,flash,render_template,request
from urllib.parse import urlparse,urljoin
from flask_login import login_user,current_user,logout_user,login_required
from myblog.models import Admin
from myblog.forms import LoginForm


auth_bp = Blueprint('auth',__name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('你已经登录','info')
        return redirect_back()
    
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remenber.data
        admin = Admin.query.first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin,remember)
                flash('你回来了','info')
                return redirect_back()
            flash('Invalid username or password.','warning')
        else:
            flash('No account.','warning')
    return render_template('auth/login.html',form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout sucess.','info')
    return redirect_back()

@auth_bp.route('/secret')
@login_required
def secret():
    return 'only logined user can see'


def redirect_back(default='blog.index',**kawrgs):
    for target in request.args.get('next'),request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default,**kawrgs))

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http','https') and ref_url.netloc == test_url.netloc