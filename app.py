from flask import Flask, redirect, request, render_template, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
import logging
from logging import Formatter, FileHandler
from forms import LoginForm, RegisterForm
from config import Config

# Створюємо екземпляр додатку Flask
app = Flask(__name__)
from models import User,users_collection
# Конфігурація Flask (наприклад, секретний ключ)
app.config.from_object(Config)


# Імпортуємо функції з моделей MongoDB


# Імпортуємо сторінки для різних розділів (наприклад, урокі, адмін-панель)
from uroki.uroki import uroki
app.register_blueprint(uroki, url_prefix='/uroki')
from admin.admin import admin
app.register_blueprint(admin, url_prefix='/admin')

# Ініціалізація Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Клас для представлення користувача у Flask-Login
class LoginUser(UserMixin):
    @property
    def is_admin(self):
        return self.is_authenticated and self.id == 'admin'

# Завантаження користувача для Flask-Login

@login_manager.user_loader
def user_loader(username):
    user = User.get_user_by_username(username, users_collection)  # Pass users_collection
    if user is None:
        return None

    login_user = LoginUser()
    login_user.id = user.get('username')
    login_user.username = user.get('username')
    # Додайте інші поля користувача, які вам потрібні

    return login_user

# Головна сторінка
@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')

# Сторінка "Про нас"
@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

# Сторінка профілю користувача
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
        username = form.username.data
        password = form.password.data

        # Fetch user by username
        user = User.get_user_by_username(username, users_collection)

        # Validate credentials (if user is found)
        if user:
            if user.checkPassword(password):
                # User authenticated successfully
                login_user(user, remember=form.remember_me.data)  # Use user object for login
                return redirect(url_for('home'))
            else:
                # Invalid password
                flash('Invalid password.', 'danger')  # Use a category for styling
        else:
            # Username not found
            flash('Invalid username or password.', 'danger')  # More generic message

    return render_template('forms/login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        if not User.add_user_to_database(form.username.data, form.email.data, form.password.data, users_collection):  # Pass users_collection
            return redirect(url_for('register'))
        flash('Тепер ви зареєстровані та можете увійти!', 'success')
        return redirect(url_for('login'))
    return render_template('forms/register.html', form=form)
# Вихід з облікового запису
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Ви успішно вийшли.", "success")
    return redirect(url_for('home'))

# Обробники помилок
@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

# Налаштування логування
if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# Запуск додатку
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)