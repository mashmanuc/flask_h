from pymongo import MongoClient
import os
import sqlite3

# Підключення до MongoDB
mongo_key = os.environ.get('mongo_key')
# print(mongo_key)
client = MongoClient("mongodb+srv://mashmanuc:1WTFCFWcW5gbAYCU@cluster0.vbybi6i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
mongo_db = client['users']
collection_predmet = mongo_db['predmet']
collection_claass = mongo_db['claass']
collection_tema_test = mongo_db['tema_test']

# Підключення до SQLite
sqlite_conn = sqlite3.connect('basaSS.db')
cursor = sqlite_conn.cursor()

# Витягнення даних з бази даних SQLite і запис у MongoDB
cursor.execute("SELECT * FROM Predmet")
predmets = cursor.fetchall()

for predmet in predmets:
    predmet_id, predmet_name = predmet
    claass_list = []

    cursor.execute("SELECT id, claass_name FROM Claass WHERE predmet_id = ?", (predmet_id,))
    claasses = cursor.fetchall()

    for claass in claasses:
        claass_id, claass_name = claass
        tema_test_list = []

        cursor.execute("SELECT id, test_name FROM Tema_test WHERE claass_id = ?", (claass_id,))
        tema_tests = cursor.fetchall()

        for tema_test in tema_tests:
            tema_test_id, test_name = tema_test
            test_list = []

            # Перевірка наявності таблиці Test
            cursor.execute("PRAGMA table_info(Test)")
            table_info = cursor.fetchall()
            if table_info:
                cursor.execute("SELECT id, num_quest, quest_img, quest_text, ans_data, vidpov FROM Test WHERE tema_test_id = ?", (tema_test_id,))
                tests = cursor.fetchall()

                for test in tests:
                    test_id, num_quest, quest_img, quest_text, ans_data, vidpov = test
                    test_data = {
                        'id': test_id,
                        'num_quest': num_quest,
                        'quest_img': quest_img,
                        'quest_text': quest_text,
                        'ans_data': ans_data,
                        'vidpov': vidpov,
                        'tema_test_id': tema_test_id
                    }
                    test_list.append(test_data)

            tema_test_data = {
                'id': tema_test_id,
                'test_name': test_name,
                'claass_id': claass_id,
                'test_list': test_list
            }
            tema_test_list.append(tema_test_data)
            collection_tema_test.insert_one(tema_test_data)

        claass_data = {
            'id': claass_id,
            'claass_name': claass_name,
            'predmet_id': predmet_id,
            'tema_test_list': tema_test_list
        }
        claass_list.append(claass_data)
        collection_claass.insert_one(claass_data)

    predmet_data = {
        'id': predmet_id,
        'predmet_name': predmet_name,
        'claass_list': claass_list
    }
    print(f"Predmet data: {predmet_data}")
    collection_predmet.insert_one(predmet_data)

sqlite_conn.close()
print("Дані було успішно перенесено у MongoDB!")