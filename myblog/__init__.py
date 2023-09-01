import os
import click
from .blueprints import admin,auth,blog
from .extensions import db,bootstrap,login_manager,mail,migrate,csrf
from .models import Admin,Category,Project,Comment,Post
from .settings import config
from flask import  Flask,render_template,request,url_for
from flask_login import current_user
from flask_wtf.csrf import CSRFError
import datetime

import logging
from logging.handlers import SMTPHandler,RotatingFileHandler

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG','development')
    
    app = Flask('myblog')
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprint(app)
    register_commands(app)
    register_errors(app)
    register_templates_context(app)
    return app
    
def register_extensions(app):
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app,db)
    csrf.init_app(app)
    

def register_logging(app):
    class RequestFormatter(logging.Formatter):
        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)
    
    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/bluelog.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    mail_handler = SMTPHandler(
        mailhost=app.config['MAIL_SERVER'],
        fromaddr=app.config['MAIL_USERNAME'],
        toaddrs=['MAIL_USERNAME'],
        subject='myBlog Application Error',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(request_formatter)

    if not app.debug:
        app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)


def register_blueprint(app):
    app.register_blueprint(blog.blog_bp)
    app.register_blueprint(admin.admin_bp,url_prefix = '/admin')
    app.register_blueprint(auth.auth_bp,url_prefix = '/auth')
    
def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)

def register_commands(app):
    @app.cli.command()
    @click.option('--category',default=10,help='make categroy,10')
    @click.option('--post',default=50)
    @click.option('--comment',default=500)
    @click.option('--project',default=3)
    def forge(category:int, post:int, comment:int,project:int) -> None:
        from .fakes import fake_admin,fake_categories,fake_comments,fake_posts,fake_project
    
        db.drop_all()
        db.create_all()
    
        click.echo('init admin...')
        fake_admin()
        click.echo('init categories...')
        fake_categories(category)
        click.echo('init post...')
        fake_posts(post)
        click.echo('init comments...')
        fake_comments(comment)
        click.echo('init projects...')
        fake_project(project)
        
        click.echo('Done!')
    
    
    @app.cli.command()
    @click.option('--username',prompt=True)
    @click.password_option()
    def init(username,password):
        '''创建管理员账户'''
        click.echo('init db...')
        db.create_all()
        
        admin = Admin.query.first()
        if admin:
            click.echo('the account for admin already exists,updating...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating account...')
            admin = Admin(
                username= username,
                blog_title = "YellowBean's blog",
                blog_sub_title = '可恶被你发现了',
                name = 'Admin',
                about = 'biubiubiubiu'
            )
            admin.set_password(password)
        db.session.add(admin)
        
        category = Category.query.first()
        if category is None:
            click.echo('Creating category')
            category = Category(name='default')
            db.session.add(category)
            
        
        db.session.commit()
        click.echo('Done.')
         
        

def register_templates_context(app:Flask):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first() 
        categories = Category.query.order_by(Category.name).all()
        projects = Project.query.order_by(Project.begin_time).all()
        dt = datetime.timedelta(hours=8)
        now = Post.query.filter_by(title = 'Now').first()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(admin=admin, categories=categories,
                    projects = projects,unread_comments=unread_comments,dt=dt,now=now)


def register_errors(app:Flask):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html',description=e.description),400
    