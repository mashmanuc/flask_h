from itertools import zip_longest
import base64
from bson import ObjectId
from flask import Blueprint, render_template, make_response, redirect, url_for, request
from pymongo import MongoClient
from config import MONGO_KEY

# Підключення до бази даних
client = MongoClient(MONGO_KEY)
title = 'Тести по темах'
nmt_t = Blueprint('nmt_test', __name__, template_folder='templates')

user_name='mamama444'
collection_names = client['zno_test_aa'].list_collection_names()
cleaned_collection_names = [name.strip('\n') for name in collection_names]

collection = client['zno_test_aa']['user_results']
for i in collection:
    print(i)
