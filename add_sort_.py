from cread_app import app, db
import pymongo
import datetime 
# client=pymongo.MongoClient("mongodb+srv://mashmanuc:1WTFCFWcW5gbAYCU@cluster0.vbybi6i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# db=client.test
# coll=db.users
import sqlite3
from model import get_all_items, Predmet, Claass, Tema_test, Test, find_temi_by_test, find_temi_by_predmet, find_Tema_test_by_id, ob1_ob2, mass_ans, first_tema_test, find_temy_site, min_max_test_id, tes_ans, find_test
# Підключення до SQLite
sqlite_conn = sqlite3.connect('basaSS.db')
cursor = sqlite_conn.cursor()

# Створення контексту застосунку Flask
with app.app_context():
    pre = find_Tema_test_by_id(1)
    # print(pre)
with app.app_context():
    mass=find_temy_site()
# print(mass)
def all_items(class_):
    
        try:
            with app.app_context():
                items = class_.query.all()
            #     print(type(items))
            # if class_ == Predmet:
            #     for item in items:
            #         item.claass_list
            # elif class_ == Claass:
            #     for item in items:
            #         item.tema_test_list
            return items
        except Exception as e:
            print(f"Помилка отримання всіх записів: {e}")
            return []
for i in all_items(Predmet):
     print(i.predmet_name)