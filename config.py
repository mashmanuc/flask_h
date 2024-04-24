import os
from dotenv import load_dotenv
load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

MONGO_KEY = os.environ.get('MONGO_KEY')

class Config:
 
    SECRET_KEY = os.environ.get('SECRET_KEY')
    