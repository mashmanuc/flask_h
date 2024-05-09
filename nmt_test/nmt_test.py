from itertools import zip_longest  # Імпортуємо функцію zip_longest з модуля itertools
import base64  # Імпортуємо модуль base64 для кодування та декодування даних у форматі Base64
from bson import ObjectId  # Імпортуємо клас ObjectId з модуля bson для роботи з ідентифікаторами MongoDB
from flask import Blueprint, render_template, make_response, redirect, url_for, request  # Імпортуємо необхідні класи та функції з модуля flask
from pymongo import MongoClient  # Імпортуємо клас MongoClient з модуля pymongo для підключення до MongoDB
from config import MONGO_KEY  # Імпортуємо ключ підключення до MongoDB з файлу config.py

from flask_login import current_user
# Підключення до бази даних
client = MongoClient(MONGO_KEY)  # Створюємо об'єкт MongoClient з використанням ключа підключення
clolection = 'zno_test_aa'  # Задаємо назву колекції в MongoDB


nmt_t = Blueprint('nmt_test', __name__, template_folder='templates')  # Створюємо новий Blueprint для маршрутів, пов'язаних з тестами
import logging  # Імпортуємо модуль logging для логування

# Налаштування логера
logger = logging.getLogger(__name__)  # Створюємо новий логер
logger.setLevel(logging.ERROR)  # Встановлюємо рівень логування ERROR


title = 'Тести по темах'  # Задаємо назву для тестів
@nmt_t.route('/get_image_data/<image_id>')
def get_image_data(image_id):
    """
    Функція для отримання зображення з бази даних MongoDB за його ідентифікатором.

    Вхідні дані:
    - image_id (str): Ідентифікатор зображення в форматі рядка.

    Вихідні дані:
    - (str) або None: Закодоване в форматі Base64 зображення або None, якщо зображення не знайдено.
    """
    try:
        image_id = ObjectId(image_id)  # Перетворюємо рядок на об'єкт ObjectId
    except TypeError:
        # print(f"Невірний ідентифікатор зображення: {image_id}")
        return None

    image_data = client[clolection]['images'].find_one({'_id': image_id})  # Знаходимо документ з зображенням у колекції 'images'
    if image_data:
        image_binary = image_data.get('data')  # Отримуємо бінарні дані зображення
        if image_binary:
            return base64.b64encode(image_binary).decode('utf-8')  # Кодуємо бінарні дані в Base64 і повертаємо закодоване зображення
        else:
            # print(f"Документ з ідентифікатором {image_id} не містить бінарних даних зображення")
            return None
    else:
        # print(f"Зображення з ідентифікатором {image_id} не знайдено в базі даних")
        return None

@nmt_t.route('/')
def index_nmt():
    """
    Функція для відображення головної сторінки з переліком колекцій тестів.

    Вхідні дані: немає.

    Вихідні дані:
    - Rendered template: Згенерований HTML-шаблон з переліком колекцій тестів.
    """
    # Отримуємо список назв колекцій
    collection_names = client[clolection].list_collection_names()

    # Видаляємо колекції 'images' та 'user_results' зі списку
    cleaned_collection_names = [name.strip('\n') for name in collection_names if name not in ['images', 'user_results']]

    # Рендеримо шаблон з переліком колекцій
    return render_template('nmt_test/index_nmt_test.html', collection_names=cleaned_collection_names)

@nmt_t.route('/nmt_tema/<collection_name>')
def nmt_test_tema(collection_name):
    """
    Функція для відображення першого питання тесту з вказаної колекції.

    Вхідні дані:
    - collection_name (str): Назва колекції, з якої потрібно отримати перше питання тесту.

    Вихідні дані:
    - Rendered template або рядок "Документ не знайдено": Згенерований HTML-шаблон з першим питанням тесту або повідомлення про відсутність документа.
    """
    sanitized_collection_name = collection_name.replace('\n', '')  # Видаляємо символи нового рядка з назви колекції
    collection = client[clolection][sanitized_collection_name]  # Отримуємо колекцію з бази даних
    test_data = collection.find_one({'question_number': '1'})  # Вибір першого завдання

    if test_data:
        question_images = [get_image_data(image_id) for image_id in test_data.get('question_images', [])]  # Отримуємо зображення питання
        answer_images = [get_image_data(image_id) for image_id in test_data.get('answer_images', [])]  # Отримуємо зображення відповідей

        test_data['question_images'] = question_images  # Додаємо зображення питання до даних тесту
        test_data['answer_images'] = answer_images  # Додаємо зображення відповідей до даних тесту

        min_question_number = collection.find().sort('question_number', 1).limit(1)[0]['question_number']  # Отримуємо номер першого питання
        max_question_number = collection.find().sort('question_number', -1).limit(1)[0]['question_number']  # Отримуємо номер останнього питання

        # Знайдемо дані про відповіді користувача для цієї колекції тестів
        user_name = current_user.name if current_user.is_authenticated else 'Anonymous'
        user_answers = {
            result['question_number']: result['user_answer_index']
            for result in client[clolection]['user_results'].find(
                {'collection_name': sanitized_collection_name, 'user_name': user_name}
            )
        }

        return render_template('nmt_test/ppage_nmt_test.html',
                                test_data=test_data,
                                collection_name=collection_name,
                                min_question_number=int(min_question_number),
                                max_question_number=int(max_question_number),
                                user_answers=user_answers)  # Рендеримо шаблон з даними першого питання
    else:
        return "Документ не знайдено"

@nmt_t.route('/show_test/<collection_name>/<question_number>')
def show_test(collection_name, question_number):
    """
    Функція для відображення тесту з вказаної колекції.

    Вхідні дані:
    - collection_name (str): Назва колекції, з якої потрібно отримати тест.
    - question_number (str): Номер питання тесту.

    Вихідні дані:
    - Rendered template або помилка 404: Згенерований HTML-шаблон з тестом або повідомлення про відсутність документа.
    """
    sanitized_collection_name = collection_name.replace('\n', '')  # Видаляємо символи нового рядка з назви колекції

    try:
        question_number = int(question_number)  # Перетворюємо номер питання в ціле число
    except ValueError:
        return render_template('404.html'), 404  # Якщо номер питання не може бути перетворений в ціле число, видаємо помилку 404

    collection = client[clolection][sanitized_collection_name]  # Отримуємо колекцію з бази даних
    test_data = collection.find_one({'question_number': str(question_number)})  # Знаходимо дані тесту за номером питання

    if test_data:
        # Отримуємо дані зображень питання та відповідей
        question_images = [get_image_data(image_id) for image_id in test_data.get('question_images', [])]
        answer_images = [get_image_data(image_id) for image_id in test_data.get('answer_images', [])]

        # Поновлюємо дані тесту з отриманими зображеннями
        test_data['question_images'] = question_images
        test_data['answer_images'] = answer_images

        # Отримуємо мінімальний та максимальний номери питань для навігації
        min_question_number = collection.find().sort('question_number', 1).limit(1)[0]['question_number']
        max_question_number = collection.find().sort('question_number', -1).limit(1)[0]['question_number']

        # Знайдемо дані про відповіді користувача для цього питання
        user_name = current_user.name if current_user.is_authenticated else 'Anonymous'
        user_answers = {
            result['question_number']: result['user_answer_index']
            for result in client[clolection]['user_results'].find(
                {'collection_name': sanitized_collection_name, 'user_name': user_name}
            )
        }

        # Передаємо дані тесту та мінімальний/максимальний номери питань до шаблону
        return render_template('nmt_test/ppage_nmt_test.html', test_data=test_data,
                               min_question_number=int(min_question_number),
                               max_question_number=int(max_question_number),
                               collection_name=collection_name,
                               user_answers=user_answers)
    else:
        return render_template('404.html'), 404  # Якщо дані тесту не знайдено, видаємо помилку 404
   

@nmt_t.route('/submit_answer_test/<collection_name>/<question_number>/<ansver_num>')
def submit_answer_test(collection_name, question_number,ansver_num):
    
    sanitized_collection_name = collection_name.replace('\n', '')
    collection = client[clolection][sanitized_collection_name]
    test_data = collection.find_one({'question_number': (question_number)})
    if test_data:
        # Отримати відповідь користувача та інші дані
        user_answer_index = ansver_num
        user_name = current_user.name if current_user.is_authenticated else 'Anonymous'
        correct_answer_index = test_data.get('correct_answer_index')

        # Перевірити, чи вже є відповідь користувача для цього питання
        existing_answer = client[clolection]['user_results'].find_one({
            'collection_name': sanitized_collection_name,
            'question_number': int(question_number),
            'user_name': user_name
        })

        # Якщо відповідь вже є, змінити її, якщо ні, зберегти нову відповідь
        if existing_answer:
            existing_answer['user_answer_index'] = int(user_answer_index)-1
            client[clolection]['user_results'].update_one(
                {'_id': ObjectId(existing_answer['_id'])},
                {'$set': {'user_answer_index': int(user_answer_index)-1}}
            )
        else:
            user_result = {
                'collection_name': sanitized_collection_name,
                'question_number': int(question_number),
                'user_name': user_name,
                'user_answer_index': int(user_answer_index)-1,
                'correct_answer_index': correct_answer_index,
                'is_correct': int(user_answer_index)-1 == correct_answer_index
            }
            client[clolection]['user_results'].insert_one(user_result)

        # Повернути на сторінку з цим же питанням
        return redirect(url_for('nmt_test.show_test', collection_name=collection_name, question_number=question_number))
    else:
        return "Документ не знайдено"

@nmt_t.route('/show_test/<collection_name>/<question_number>')
def show_test_nmt(collection_name, question_number):
    sanitized_collection_name = collection_name.replace('\n', '')
    collection = client[clolection][sanitized_collection_name]
    test_data = collection.find_one({'question_number': str(question_number)})

    if test_data:
        # Отримати дані відповідей користувача
        user_name = current_user.name if current_user.is_authenticated else 'Anonymous'
        user_answers = {
            result['question_number']: result['user_answer_index']
            for result in client[clolection]['user_results'].find(
                {'collection_name': sanitized_collection_name, 'user_name': user_name}
            )
        }

        # Отримати дані про вибрану відповідь користувача для цього питання
        selected_answer_index = user_answers.get(int(question_number), None)

        # Передати дані про відповіді користувача на сторінку тесту
        return render_template(
            'nmt_test/ppage_nmt_test.html',
            test_data=test_data,
            collection_name=collection_name,
            user_answers=user_answers,
            selected_answer_index=selected_answer_index
        )
    else:
        return "Документ не знайдено"
@nmt_t.route('/show_results/<collection_name>')
def show_results(collection_name):
    try:
        sanitized_collection_name = collection_name.replace('\n', '')
        user_results = list(client[clolection]['user_results'].find({'collection_name': sanitized_collection_name}))
        total_questions = len(user_results)

        if total_questions == 0:
            # Користувач ще не проходив цей тест
            return render_template('nmt_test/page_res.html', vids=0, temma=collection_name, total_score=0, no_results=True)

        collection = client[clolection][sanitized_collection_name]
        correct_answer = 0

        for result in user_results:
            user_answer_index = result['user_answer_index']
            correct_answer_index = result['correct_answer_index']
            if user_answer_index == correct_answer_index:
                correct_answer += 1

        test_data = collection.find_one({'question_number': '1'})

        if test_data:
            # Обчислюємо відсоток успішності
            success_percentage = (correct_answer / total_questions) * 100
            total_score = round(success_percentage * 12 / 100)
            return render_template('nmt_test/page_res.html', vids=round(success_percentage), temma=collection_name, total_score=total_score)
        else:
            return "Документ з питаннями не знайдено в базі даних", 404
    except Exception as e:
        # Логуємо помилку
        nmt_t.logger.error(f"Помилка при обробці запиту show_results: {e}")
        return "Виникла внутрішня помилка сервера", 500