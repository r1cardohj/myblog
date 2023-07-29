from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,PasswordField,\
    BooleanField,SelectField,HiddenField,IntegerField,URLField,DateTimeField
from wtforms.validators import DataRequired,Email,Length
from .models import Category

class CommentForm(FlaskForm):
    '''评论窗口'''
    author = StringField('用户名',validators=[DataRequired(),Length(1, 30)],render_kw={'placeholder':'Your Name...'})
    email = StringField('电子邮箱',validators=[DataRequired(),Length(1,254)],render_kw={'placeholder':'Your Email...'})
    body = TextAreaField('评论',validators=[DataRequired()],render_kw={'placeholder':'write something...'})
    sumbit = SubmitField('提交')


class AdminCommentForm(CommentForm):
    '''管理员评论窗口'''
    author = HiddenField()
    email = HiddenField()


class LoginForm(FlaskForm):
    '''登录窗口'''
    username = StringField('UserName',validators=[DataRequired(),Length(1,20)])
    password = PasswordField('Password',validators=[DataRequired(),Length(8,56)])
    remenber = BooleanField('Remenber me')
    submit = SubmitField()
    

class PostForm(FlaskForm):
    '''创建文章窗口'''
    title = StringField('Title',validators=[DataRequired(),Length(1,60)]) 
    category = SelectField('Category',coerce=int, 
                           default=1
                           )
    #body = PageDownField('body',validators=[DataRequired()])
    body = TextAreaField('body',validators = [DataRequired()])
    submit = SubmitField('Submit')
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]


class CategoryForm(FlaskForm):
    """创建分类窗口"""
    name = StringField('Name',validators=[DataRequired(),Length(1,20)])
    submit = SubmitField('Submit')
    

class ProjectForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired(),Length(1,20)])
    detail = StringField('Detail',validators=[DataRequired(),Length(1,255)])
    progress = IntegerField('progress',validators=[DataRequired(),Length(1,100)])
    pic_endpoint = StringField('Pic_endpoint',validators=[DataRequired(),Length(1,100)])
    url = URLField('URL',validators=[DataRequired(),Length(1,200)])
    begin_time = DateTimeField('URL')
    deadline = DateTimeField('Deadline')
    