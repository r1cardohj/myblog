from flask import Blueprint,render_template,request,current_app
from markupsafe import Markup
from myblog.models import Post

blog_bp = Blueprint('blog',__name__)

@blog_bp.route('/')
def index():
    #page =request.args.get('page', type=int)
    #per_page = current_app.config['Post_PER_Page']
    posts = Post.query.order_by(Post.timestamp.desc()).limit(10).all()
    #posts = pagination.items
    return render_template('index.html',posts=posts)