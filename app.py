



import logging
from logging import Formatter, FileHandler

from cread_app import app,db

    

from flask import redirect, request, render_template, url_for, flash 






@app.route('/')
def home():
    
        return render_template('index.html')


#----------------------------------------------------------------------------#

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)

