
from flask import Flask

import os
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)




# Створення контексту додатка перед кожним запитом


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

