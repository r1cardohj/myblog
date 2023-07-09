import os
import click
from .blueprints import admin,auth,blog
from .extensions import db,bootstrap,moment,login_manager,mail
from .models import Admin,Category
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
    def forge(category:int, post:int, comment:int) -> None:
        from .fakes import fake_admin,fake_categories,fake_comments,fake_posts
    
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
        
        click.echo('Done!')

def register_templates_context(app:Flask):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first() 
        categories = Category.query.order_by(Category.name).all()
        return dict(admin=admin, categories=categories)