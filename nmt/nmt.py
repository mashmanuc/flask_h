from flask import Blueprint, render_template, url_for, redirect, request

title = 'NMT'
nmt = Blueprint('nmt', __name__, template_folder='templates')

from model import find_temi_by_test, find_temi_by_predmet, find_Tema_test_by_id, ob1_ob2, mass_ans, first_tema_test, find_temy_site, min_max_test_id, tes_ans, find_test
from models import users_collection, user_test_collection, add_user_test, user_test, user_res_test, dinamic,   find_vid, vidsotok
from config import MONGO_KEY
from pymongo import MongoClient
client = MongoClient(MONGO_KEY)


@nmt.route('/')
def index_nmt():
    html_snippets = []
    collection_names = client['nmt_snipet'].list_collection_names()
    print(f"Collection names: {collection_names}")
    cleaned_collection_names = [name.strip('\n') for name in collection_names]
    for collection_name in collection_names:
        collection = client['nmt_snipet'][collection_name]
        doc = collection.find_one()
        if doc:
            html_snippets.append(doc['teg'])
            # print(f"Document from {collection_name}: {doc}")
    print("Rendering template...")
    return render_template('index_nmt.html', collection_names=cleaned_collection_names)


@nmt.route('/nmt_tema/<collection_name>')
def nmt_tema(collection_name):
    try:
        sanitized_collection_name = collection_name.replace('\n', '')
        collection = client['nmt_snipet']['\n'+sanitized_collection_name+'\n']
        documents = list(collection.find())
        print(documents)
        if documents:  # Проверка на наличие документов
            return render_template('nmt_tema.html', collection=documents, title=collection_name)
        else:
            return "Документы в коллекции отсутствуют"
    except Exception as e:
        print(f"Помилка отримання колекції: {e}")
        return "Помилка отримання колекції"