from flask import Blueprint,request,current_app,render_template,flash,redirect,url_for
from flask_login import login_required
from ..models import Post,Category,Comment,Project,Admin
from ..extensions import db
from .auth import redirect_back
from ..forms import PostForm,CategoryForm,ProjectForm,SettingsForm
from datetime import datetime



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


@admin_bp.post('/set-comment/<int:post_id>')
@login_required
def set_comment(post_id):
    post = Post.query.get_or_404(post_id)
    if post.can_comment:
        post.can_comment = False
        flash('Comment disable.','info')
    else:
        post.can_comment = True
        flash('Comment enable','info')
    db.session.commit()
    return redirect(url_for('blog.show_post',post_id=post_id))

@admin_bp.route('/comment/manage')
@login_required
def manage_comment():
    filter_rule = request.args.get('filter','all')
    page = request.args.get('page',1,type=int)
    per_page = current_app.config.get('COMMENT_PER_PAGE',10)
    if filter_rule == 'unread':
        filter_comments = Comment.query.filter_by(reviewed=False)
    elif filter_rule == 'admin':
        filter_comments = Comment.query.filter_by(from_admin=True)
    else:
        filter_comments = Comment.query
        
    pagination = filter_comments.order_by(Comment.timestamp.desc()).paginate(page=page,per_page=per_page)
    comments = pagination.items
    return render_template('admin/manage_comment.html',comments=comments,pagination=pagination)


@admin_bp.post('/comment/approve/<int:comment_id>')
@login_required
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.reviewed == False:
        comment.reviewed = True
        flash('Success.')
    db.session.commit()
    return redirect(url_for('admin.manage_comment',filter='unread'))


@admin_bp.post('/category/<int:category_id>/delete')
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('You can not delete the defult category','warning')
        return redirect(url_for('blog.index'))
    category.delete()
    flash('Category deleted.','success')
    return redirect(url_for('blog.index'))


@admin_bp.route('/category/new',methods=['POST','GET'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash(f'<{name}> created','success')
        return redirect(url_for('blog.category'))    
    
    return render_template('admin/new_category.html',form=form)


@admin_bp.route('/project/manage')
@login_required
def manage_project():
    return render_template('admin/manage_project.html')


@admin_bp.route('/project/new/',methods=['GET','POST'])
@login_required
def new_project():
    form = ProjectForm()
    form.begin_time.data = datetime.utcnow()
    form.deadline.data = datetime.utcnow()
    if form.validate_on_submit():
        title = form.title.data
        detail = form.detail.data
        progress = form.progress.data
        pic_endpoint = form.pic_endpoint.data
        url = form.url.data
        deadline = form.deadline.data
        project = Project(title=title,
                            detail=detail,
                            progress=progress,
                            pic_endpoint=pic_endpoint,
                            url=url,
                            deadline=deadline
                            )
        db.session.add(project)
        db.session.commit()
        flash('created.')
        redirect(url_for('admin.manage_project'))
    return render_template('admin/new_project.html',form=form)

@admin_bp.route('/project/edit/<int:project_id>',methods=['GET','POST'])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    form = ProjectForm()
    if form.validate_on_submit():
        project.title = form.title.data
        project.detail = form.detail.data
        project.progress = form.progress.data
        project.pic_endpoint = form.pic_endpoint.data
        project.url = form.url.data
        project.begin_time = form.begin_time.data
        project.deadline = form.deadline.data
        db.session.commit()
        flash('Success.','success')
        redirect(url_for('admin.manage_project'))
    form.title.data = project.title
    form.detail.data = project.detail
    form.progress.data = project.progress
    form.pic_endpoint.data = project.pic_endpoint
    form.url.data = project.url
    form.begin_time.data = project.begin_time
    form.deadline.data = project.deadline
    return render_template('admin/edit_project.html',form=form)


@admin_bp.post('/project/delete/<int:project_id>')
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('del success')
    return redirect(url_for('admin.manage_project'))


@admin_bp.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    form = SettingsForm()
    admin = Admin.query.first()
    if form.validate_on_submit():
        admin.name = form.name.data
        admin.about = form.about.data
        db.session.commit()
        flash('change.')
        return redirect(url_for('blog.about'))
    return render_template('admin/settings.html',form=form)
        