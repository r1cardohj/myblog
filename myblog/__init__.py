import os
import click
from .blueprints import admin,auth,blog
from .extensions import db,bootstrap,moment,login_manager,mail,migrate
from .models import Admin,Category,Project
from .settings import config
from flask import  Flask

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG','development')
    
    app = Flask('myblog')
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprint(app)
    register_commands(app)
    register_templates_context(app)
    return app
    
def register_extensions(app):
    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app,db)
    

def register_logging(app):
    pass

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
                about = '十三线码农,想做一些温暖的东西.'
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
        return dict(admin=admin, categories=categories,projects = projects)