


from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
import logging
from logging import Formatter, FileHandler
from forms import *
from cread_app import app,db
with app.app_context():
    from models import  get_user_by_username,add_user_to_database
    
# Створюємо контекст додатку для Flask
with app.app_context():
    # Імпортуємо функції з model.py після створення контексту додатку
    from models import *
from flask import redirect, request, render_template, url_for, flash 

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#


from uroki.uroki import uroki
app.register_blueprint(uroki, url_prefix='/uroki')
from admin.admin import admin
app.register_blueprint(admin, url_prefix='/admin')
login_manager = LoginManager()
login_manager.init_app(app)

class LoginUser(UserMixin):
    @property
    def is_admin(self):
        return self.is_authenticated and self.id == 'admin'
        # TODO: YOU NEED TO IMPLEMENT THIS!! A SUGGESTION IS ADDING A "ROLE" COLUMN TO THE USER DATABSE

@app.before_request
def create_app_context():
    with app.app_context():
        pass
@login_manager.user_loader
def user_loader(username):
    user = get_user_by_username(username)
    if user is None:
        return None

    login_user = LoginUser()
    login_user.id = user.id  # Отримуємо ID користувача з об'єкта User
    login_user.username = user.username
    # Додайте інші поля користувача, які вам потрібні

    return login_user
#----------------------------------------------------------------------------#

@app.route('/')
def home():
    
        return render_template('pages/placeholder.home.html')



@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

@app.route('/profile')
@login_required
def profile():
    if current_user.is_admin:
        return """
            Hello, {}
            <br>
            <a href="/admin/">Admin Panel?</a>
            <a href="/logout">Logout</a>
        """.format(current_user.id)
    return """
        Hello, {}
        <br>
        <a href="/logout">Logout</a>
    """.format(current_user.username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = get_user_by_username(form.username.data)
        if user and user.checkPassword(form.password.data):
            luser = LoginUser()
            luser.id = user.username
            if login_user(luser, remember=True):
                return redirect(url_for('home'))
            else: return "bad"
        else:
            flash('Invalid username or password.')
    return render_template('forms/login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        if not  add_user_to_database(form.username.data, form.email.data, form.password.data):
             return redirect(url_for('register'))
        flash('Тепер ви зареєстровані та можете увійти!', 'success')
        return redirect(url_for('login'))
    return render_template('forms/register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Ви успішно вийшли."," 'success'")
    return redirect(url_for('home'))

# Error handlers ------------------------------------------------------------#

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
@app.shell_context_processor
def make_shell_context():
    return {'db': db}
#----------------------------------------------------------------------------#

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)

