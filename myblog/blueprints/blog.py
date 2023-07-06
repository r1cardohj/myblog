from flask import Blueprint,render_template,request,current_app
from markupsafe import Markup
from myblog.models import Post,Comment

blog_bp = Blueprint('blog',__name__)

@blog_bp.route('/')
def index():
    page =request.args.get('page', type=int)
    per_page = current_app.config['POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page=page,per_page=8)
    #posts = Post.query.order_by(Post.timestamp.desc()).limit(10).all()
    posts = pagination.items
    return render_template('index.html',posts=posts,pagination = pagination)

@blog_bp.route('/post/<int:post_id>',methods = ['GET','POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    #page =request.args.get('page', type=int)
    return render_template('blog/post.html',post=post)