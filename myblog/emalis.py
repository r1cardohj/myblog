from threading import Thread
from flask import url_for,render_template
from flask_mail import Message
from .extensions import mail
from flask import current_app

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def send_mail(subject, to, template,**kwargs):
    app = current_app._get_current_object()
    message = Message(current_app.config['MAIL_SUBJECT_PREFIX'] + subject, recipients=[to])
    message.body = render_template(template + '.txt',**kwargs)
    message.html = render_template(template + '.html',**kwargs)
    #mail.send(message)
    t = Thread(target=send_async_email,args=[app,message])
    t.start()
    return t

def send_comment_mail_to_admin(post):
    post_url = url_for('blog.show_post',post_id=post.id,_external=True) + '#comments'
    send_mail(subject='New Comment',to=current_app.config['MAIL_USERNAME'],
            template='mail/new_comment',post=post,post_url=post_url)