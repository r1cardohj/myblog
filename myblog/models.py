from myblog.extensions import db
from datetime import datetime
from flask_login import UserMixin
from flask import url_for
from werkzeug.security import generate_password_hash,check_password_hash
from markdown import markdown


class Admin(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(120))
    blog_title = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(100))
    name = db.Column(db.String(30))
    about = db.Column(db.Text)
    
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    
    def validate_password(self,password): 
        return check_password_hash(self.password_hash,password) 

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    posts = db.relationship('Post',back_populates='category')
    
    def delete(self):
        default_category = Category.query.get(1)
        posts = self.posts[:]
        for post in posts:
            post.category = default_category
        db.session.delete(self)
        db.session.commit()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60),unique =True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    upd_timestamp = db.Column(db.DateTime)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    category = db.relationship('Category',back_populates='posts')
    comments = db.relationship('Comment',back_populates = 'post', cascade='all,delete-orphan')
    can_comment = db.Column(db.Boolean,default=True)
    #summary = db.Column(db.String(255))
    
    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        target.body_html = markdown(value, output_format='html',extensions=['markdown.extensions.fenced_code',
                                                                            'markdown.extensions.codehilite',
                                                                            'markdown.extensions.toc',
                                                                            'markdown.extensions.tables'])

db.event.listen(Post.body, 'set', Post.on_changed_body)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow, index=True)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    post = db.relationship('Post',back_populates ='comments')
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replied = db.relationship('Comment',back_populates='replies', remote_side=[id])
    replies = db.relationship('Comment',back_populates='replied',cascade='all')
    
    


class Project(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),unique =True)
    detail = db.Column(db.String(255))
    progress = db.Column(db.Float)
    pic_endpoint = db.Column(db.String(100))
    url = db.Column(db.Text)
    begin_time = db.Column(db.DateTime,default=datetime.utcnow)
    deadline = db.Column(db.DateTime)


class Subscriber(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(254),unique = True)