from flask import flash

from passlib.hash import sha256_crypt

from datetime import datetime
from flask_login import UserMixin


# DEFINE YOUR MODELS HERE

# app = Flask(__name__)
# app.config.from_object('config')
# db.init_app(app)

from cread_app import db,app,create_tables



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def checkPassword(self, entered_password):
        return sha256_crypt.verify(entered_password, self.password)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = sha256_crypt.encrypt(password)

        return None
    def get_id(self):
        return str(self.id)

class User_test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_quest=db.Column(db.Integer, nullable=False)
    users_id = db.Column(db.Integer, nullable=False)
    tema_test_id =  db.Column(db.Integer, nullable=False)
    test_id = db.Column(db.Integer, nullable=False)
    vid = db.Column(db.String(120), nullable=False)
    pr_vid= db.Column(db.String(120), nullable=False)
    date_completed = db.Column(db.DateTime, default=datetime.utcnow)



    def __init__(self, users_id,num_quest,tema_test_id, test_id,  vid,  pr_vid  ):
            self.users_id = users_id
            self.num_quest=num_quest
            self.tema_test_id  = tema_test_id
            self.test_id = test_id
            self.vid = vid
            self.pr_vid  = pr_vid
# def add_user_test(users_id, tema_test_id, test_id, vid, pr_vid):
#     new_user_test = User_test(users_id=users_id, tema_test_id=tema_test_id, test_id=test_id, vid=vid, pr_vid=pr_vid)
#     db.session.add(new_user_test)
#     db.session.commit()
create_tables()
def add_user_test(users_id,num_quest, tema_test_id, test_id, vid, pr_vid):
    # Перевірка, чи існує вже запис для користувача і номера тесту
    existing_record = User_test.query.filter_by(users_id=users_id, test_id=test_id).first()

    if existing_record:
        # Якщо запис існує, змінюємо його значення
        existing_record.vid = vid
        existing_record.pr_vid = pr_vid
    else:
        # Якщо запису немає, додаємо новий запис
        new_user_test = User_test(users_id=users_id,num_quest=num_quest, tema_test_id=tema_test_id, test_id=test_id, vid=vid, pr_vid=pr_vid)
        db.session.add(new_user_test)

    # Зберігаємо зміни в базі даних
    db.session.commit()
def user_test(users_id, tema_test_id):
    # Перевірка, чи існує вже запис для користувача і номера тесту
    record = User_test.query.filter_by(users_id=users_id, tema_test_id=tema_test_id).all()

    if record:
       return [ (m.test_id , m.vid, (m.num_quest.split()[-1]) ) for m in record  ]

def user_res_test(users_id, tema_test_id):
    user_test_results = User_test.query.filter_by(users_id=users_id, tema_test_id=tema_test_id).order_by(User_test.test_id.asc()).all()
    return user_test_results

def dinamic(users_id, tema_test_id):
    record = User_test.query.filter_by(users_id=users_id, tema_test_id=tema_test_id).all()

    if record:
       return [ m.test_id  for m in record  ]


def get_user_by_username(username):
   
    user = User.query.filter_by(username=username).first()
    return user

def add_user_to_database(username, email, password):
    try:
        user = User(username, email, password)
        db.session.add(user)
        db.session.commit()
        flash('Тепер ви зареєстровані та можете увійти!', 'success')
        return True
    except Exception as e:
        db.session.rollback()  # Відміна транзакції в разі помилки
        flash('Error: User already exists.')
        return False

def user_t_ans(users_id, tema_test_id):
    # Перевірка, чи існує вже запис для користувача і номера тесту
    record = User_test.query.filter_by(users_id=users_id, tema_test_id=tema_test_id).all()

    if record:
       return [ (m.test_id, m.vid) for m in record  ]

def find_vid(users_id, tema_test_id, test_id):
    # Використовуйте метод query вашого ORM для пошуку відповідного запису в базі даних.
    user_test_record = User_test.query.filter_by(users_id=users_id, tema_test_id=tema_test_id, test_id=test_id).first()

    # Перевірте, чи знайдено відповідний запис.
    if user_test_record:
        return user_test_record.vid
    else:
        return None  # Або ви можете повернути яке-небудь значення за замовчуванням або порожній рядок.


def vidsotok(users_id, tema_test_id):
    ress = user_res_test(users_id, tema_test_id)
    summa = 0
    for res in ress:
        print(res.vid)
        print(res.pr_vid)
        # Вирівнюємо рядки за довжиною
        len_diff = len(res.vid) - len(res.pr_vid)
        if len_diff > 0:
            res.pr_vid = res.pr_vid.ljust(len(res.vid), ' ')
        elif len_diff < 0:
            res.vid = res.vid.ljust(len(res.pr_vid), ' ')

        # Додатковий вивід для аналізу
        print(f"Length vid: {len(res.vid)}, Length pr_vid: {len(res.pr_vid)}")
        print(f"Чи дорівнює vid pr_vid? {res.pr_vid.lower() == res.vid.lower()}")

        if res.pr_vid.lower() == res.vid.lower():
            print(summa)
            summa += 1
    print(summa)

    vid = round((summa / len(ress)) * 100)
    return vid








with app.app_context():
    db.create_all()
