from flask import Blueprint,request,current_app,render_template,flash,redirect,url_for
from flask_login import login_required
from ..models import Post,Category,Comment
from ..extensions import db
from .auth import redirect_back
from ..forms import PostForm



admin_bp = Blueprint('admin',__name__)

@admin_bp.route('/post/manage')
@login_required
def manage_post():
    page = request.args.get('page',1,type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page = page,per_page=current_app.config.get('MANAGE_POST_PER_PAGE',20))
    posts = pagination.items
    return render_template('admin/manage_post.html',pagination = pagination,
                           posts = posts,page=page)


@admin_bp.route('/post/delete/<int:post_id>',methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f'文章 《{post.title}》 已删除','success')
    return redirect_back()


@admin_bp.route('/post/edit/<int:post_id>',methods=['GET','POST'])
@login_required
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category = Category.query.get(form.category.data)
        db.session.commit()
        flash(f'文章 《{post.title} 已修改.》','success')
        return redirect(url_for('blog.show_post',post_id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category_id
    return render_template('admin/edit_post.html',form=form)


@admin_bp.route('post/new',methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.category.data)
        post = Post(title=title,body=body,category=category)
        db.session.add(post)
        db.session.commit()
        flash('文章已创建','success')
        return redirect(url_for('blog.show_post',post_id=post.id))
    return render_template('admin/new_post.html',form = form)


@admin_bp.route('commemt/delete/<int:comment_id>',methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('评论已删除')
    return redirect_back()