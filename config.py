import os
from dotenv import load_dotenv
load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

# MONGO_KEY = os.environ.get('MONGO_KEY')
MONGO_KEY='mongodb+srv://mashmanuc:1WTFCFWcW5gbAYCU@cluster0.vbybi6i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

class Config:
 
    SECRET_KEY = os.environ.get('SECRET_KEY')
    