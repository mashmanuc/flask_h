# from itertools import zip_longest
# import base64
# from bson import ObjectId
# from flask import Blueprint, render_template, make_response, redirect, url_for, request
# from pymongo import MongoClient
# from config import MONGO_KEY

# # Підключення до бази даних
# client = MongoClient(MONGO_KEY)
# title = 'Тести по темах'
# nmt_t = Blueprint('nmt_test', __name__, template_folder='templates')
# import logging

# # Налаштування логера
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.ERROR)
# # @nmt_t.route('/get_image/<image_id>')
# # def get_image(image_id):
# #     image_data = client['zno_test_aa']['images'].find_one({'_id': ObjectId(image_id)})
# #     if image_data:
# #         image_binary = image_data['data']
# #         response = make_response(image_binary)
# #         response.headers.set('Content-Type', 'image/jpeg')
# #         return response
# #     return None
# @nmt_t.route('/get_image_data/<image_id>')
# def get_image_data(image_id):
#     try:
#         image_id = ObjectId(image_id)
#     except TypeError:
#         # print(f"Невірний ідентифікатор зображення: {image_id}")
#         return None

#     image_data = client['zno_test_aa']['images'].find_one({'_id': image_id})
#     if image_data:
#         image_binary = image_data.get('data')
#         if image_binary:
#             return base64.b64encode(image_binary).decode('utf-8')
#         else:
#             # print(f"Документ з ідентифікатором {image_id} не містить бінарних даних зображення")
#             return None
#     else:
#         # print(f"Зображення з ідентифікатором {image_id} не знайдено в базі даних")
#         return None

# @nmt_t.route('/')
# def index_nmt():
#     collection_names = client['zno_test_aa'].list_collection_names()
#     cleaned_collection_names = [name.strip('\n') for name in collection_names]
#     return render_template('nmt_test/index_nmt_test.html', collection_names=cleaned_collection_names)




# @nmt_t.route('/nmt_tema/<collection_name>')
# def nmt_test_tema(collection_name):
#     # try:
#         question_number=1
#         sanitized_collection_name = collection_name.replace('\n', '')
#         collection = client['zno_test_aa'][sanitized_collection_name]
#         test_data = collection.find_one({'question_number': int(question_number)})

#         if test_data:
#             question_images = [get_image_data(image_id) for image_id in test_data.get('question_images', [])]
#             answer_images = [get_image_data(image_id) for image_id in test_data.get('answer_images', [])]

#             test_data['question_images'] = question_images
#             test_data['answer_images'] = answer_images

#             min_question_number = collection.find().sort('question_number', 1).limit(1)[0]['question_number']
#             max_question_number = collection.find().sort('question_number', -1).limit(1)[0]['question_number']

#             return render_template('nmt_test/ppage_nmt_test.html', test_data=test_data, collection_name=collection_name, min_question_number=min_question_number, max_question_number=max_question_number)
#         else:
#             return redirect(url_for('nmt_test.index_nmt'))
#     # except Exception as e:
#     #     logger.error(f"Помилка отримання документа: {e}")
#     #     return redirect(url_for('nmt_test.index_nmt'))

# @nmt_t.route('/show_test/<collection_name>/<question_number>')
# def show_test(collection_name, question_number):
#     try:
#         sanitized_collection_name = collection_name.replace('\n', '')
#         collection = client['zno_test_aa'][sanitized_collection_name]
#         test_data = collection.find_one({'question_number': int(question_number)})

#         if test_data:
#             question_images = [get_image_data(image_id) for image_id in test_data.get('question_images', [])]
#             answer_images = [get_image_data(image_id) for image_id in test_data.get('answer_images', [])]

#             test_data['question_images'] = question_images
#             test_data['answer_images'] = answer_images

#             # Отримати мінімальний та максимальний номери питань для навігації
#             min_question_number = collection.find().sort('question_number', 1).limit(1)[0]['question_number']
#             max_question_number = collection.find().sort('question_number', -1).limit(1)[0]['question_number']

#             # Передати дані тесту та мінімальний/максимальний номери питань до шаблону
#             return render_template('nmt_test/show_test.html', test_data=test_data,
#                                    min_question_number=min_question_number,
#                                    max_question_number=max_question_number,
#                                    collection_name=collection_name)
#         else:
#             return "Документ не знайдено"
#     except Exception as e:
#         print(f"Помилка отримання документа: {e}")
#         return "Помилка отримання документа"

# @nmt_t.route('/submit_answer/<collection_name>/<question_number>', methods=['POST'])
# def submit_answer(collection_name, question_number):
#     try:
#         sanitized_collection_name = collection_name.replace('\n', '')
#         collection = client['zno_test_aa'][sanitized_collection_name]
#         test_data = collection.find_one({'question_number': int(question_number)})

#         if test_data:
#             user_answer = request.form.get('answer')
#             correct_answer_index = test_data.get('correct_answer_index')

#             # Зберегти результат користувача в базі даних
#             # ...

#             next_question_number = int(question_number) + 1
#             return redirect(url_for('nmt_test.show_test', collection_name=collection_name, question_number=next_question_number))
#         else:
#             return "Документ не знайдено"
#     except Exception as e:
#         print(f"Помилка отримання документа: {e}")
#         return "Помилка отримання документа"