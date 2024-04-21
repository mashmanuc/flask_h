
from flask import Flask

import os
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
db.init_app(app)

# Створення контексту додатка перед кожним запитом
def create_tables():
    with app.app_context():
        db.create_all()


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

