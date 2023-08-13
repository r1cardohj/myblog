from flask import Blueprint,render_template,request,current_app,flash,redirect,url_for
from markupsafe import Markup
from myblog.models import Post,Comment,Category,Subscriber
from myblog.forms import CommentForm,AdminCommentForm,SubscribeForm
from flask_login import current_user
from myblog.emalis import send_comment_mail_to_admin
from myblog.extensions import db

blog_bp = Blueprint('blog',__name__)

@blog_bp.route('/')
def index():
    page =request.args.get('page', type=int)
    per_page = current_app.config['POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page=page,per_page=10)
    #posts = Post.query.order_by(Post.timestamp.desc()).limit(10).all()
    posts = pagination.items
    return render_template('blog/index.html',posts=posts,pagination = pagination)

@blog_bp.route('/post/<int:post_id>',methods = ['GET','POST'])
def show_post(post_id):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    page =request.args.get('page', type=int)
    per_page = current_app.config.get('COMMENT_PER_PAGE',8) 
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.asc()).paginate(page=page,per_page=per_page)
    comments = pagination.items
    if current_user.is_authenticated:
        form = AdminCommentForm()
        form.author.data = current_user.name
        form.email.data = current_app.config['MAIL_USERNAME']
        from_admin = True
        reviewed = True
    else:
        form = CommentForm()
        from_admin = False
        reviewed = False
        
    if form.validate_on_submit():
        author = form.author.data
        email = form.author.data
        body = form.body.data
        replied_id = request.args.get('reply')
        
        comment = Comment(
            author=author,email=email,body=body,
            from_admin=from_admin,post=post,reviewed=reviewed
        )
        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
        #发邮件给用户吗?
        db.session.add(comment)
        db.session.commit()
        if current_user.is_authenticated:
            flash('评论已发布','success')
        else:
            flash('评论已提交,请耐心等待审核','info')
            send_comment_mail_to_admin(post)
        return redirect(url_for('blog.show_post',post_id=post_id))
    return render_template('blog/post.html',post=post,pagination=pagination,comments=comments,form=form)


@blog_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    return redirect(url_for('blog.show_post',post_id=comment.post_id,reply=comment_id,author=comment.author)+'#comment-form')


@blog_bp.route('/category')
def category():
    return render_template('blog/category.html')


@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    posts = Post.query.filter_by(category_id=category_id).order_by(Post.timestamp.desc())
    return render_template('blog/category_detail.html',category=category,posts = posts)


@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')

@blog_bp.route('/coffee')
def coffee():
    return render_template('blog/coffee.html')

@blog_bp.route('/subscribe',methods=['GET','POST'])
def subscribe():
    form = SubscribeForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        sub = Subscriber(name=name,email=email)
        db.session.add(sub)
        db.session.commit()
        flash('订阅成功')
        redirect(url_for('blog.index'))
    return render_template('blog/subscribe.html',form=form)

@blog_bp.route('/logmyself',methods=['GET'])
def logmyself():
    posts = Post.query.order_by(Post.timestamp.desc())
    years = Post.query.order_by(Post.timestamp.desc())
    return render_template('blog/log.html',posts = posts)