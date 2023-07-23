from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,PasswordField,BooleanField,SelectField,HiddenField
from wtforms.validators import DataRequired,Email,Length

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
    category = SelectField('Category',coerce=int, default=1)
    body = TextAreaField('body',validators=[DataRequired()])
    submit = SubmitField('Submit')