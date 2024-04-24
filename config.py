import os
from dotenv import load_dotenv
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

MONGO_KEY = os.environ.get('MONGO_KEY')

class Config:
    
    
   
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # SECRET_KEY ='dFt5Fn3CZEFnbj3hhf0000000eZ555555dRsXS9UhkLaH3q3'
    
   
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
    #     'postgres://', 'postgresql://') or \
    #     'sqlite:///' + os.path.join(basedir, 'basaSS.db')
    # LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # ADMINS = ['your-email@example.com']
    # LANGUAGES = ['en', 'es']
    # MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    # ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    # REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    # POSTS_PER_PAGE = 25
    # mongo--1WTFCFWcW5gbAYCU
