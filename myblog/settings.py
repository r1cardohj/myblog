import os
import sys

baseidr = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

WIN = sys.platform.startswith('win')
if WIN:  
    prefix = 'sqlite:///'
else:  
    prefix = 'sqlite:////'

class BaseConfig(object):
    SECRET_KEY = os.getenv('SERCERT_KEY','sercet string')   
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POST_PER_PAGE = 10
    #邮箱配置
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Yellow Bean',os.getenv('MAIL_USERNAME'))
    MAIL_SUBJECT_PREFIX = 'MyBlog:'



class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(baseidr,'data-dev.db')

    
class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLE = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',prefix + os.path.join(baseidr,'data.db'))


config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig
}    