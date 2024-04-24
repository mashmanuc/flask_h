from pymongo import MongoClient
import os

# Підключення до MongoDB
mongo_key = os.environ.get('mongo_key')
client = MongoClient("mongodb+srv://mashmanuc:1WTFCFWcW5gbAYCU@cluster0.vbybi6i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
mongo_db = client['users']
collection_predmet = mongo_db['predmet']
collection_claass = mongo_db['claass']
collection_tema_test = mongo_db['tema_test']
collection_tests = mongo_db['tests']
collection_tema_site = mongo_db['tema_site']

def add_predmet(predmet_name):
    try:
        predmet_data = {'predmet_name': predmet_name}
        result = collection_predmet.insert_one(predmet_data)
        return result.inserted_id
    except Exception as e:
        print(f"Помилка додавання предмету: {e}")
        return None

def add_claass(claass_name, predmet_id):
    try:
        claass_data = {'claass_name': claass_name, 'predmet_id': predmet_id}
        result = collection_claass.insert_one(claass_data)
        return result.inserted_id
    except Exception as e:
        print(f"Помилка додавання класу: {e}")
        return None

def add_Tema_test(test_name, claass_id):
    try:
        tema_test_data = {'test_name': test_name, 'claass_id': claass_id, 'test_list': []}
        result = collection_tema_test.insert_one(tema_test_data)
        return result.inserted_id
    except Exception as e:
        print(f"Помилка додавання теми тесту: {e}")
        return None

def add_oun_temy_site(tema_test_id):
    try:
        tema_site_data = {'tema_test_id': tema_test_id}
        collection_tema_site.insert_one(tema_site_data)
    except Exception as e:
        print(f"Помилка додавання теми на сайт: {e}")

def find_temy_site():
    try:
        tema_tests = collection_tema_site.find({}, {'tema_test_id': 1, '_id': 0})
        tema_test_ids = [doc['tema_test_id'] for doc in tema_tests]
        tema_tests_data = list(collection_tema_test.find({'id': {'$in': tema_test_ids}}))
        return tema_tests_data
    except Exception as e:
        print(f"Помилка пошуку тем на сайті: {e}")
        return []

def ob1_ob2(predmet_id=1):
    try:
        predmet = collection_predmet.find_one({'id': predmet_id})
        claass_list = list(collection_claass.find({'predmet_id': predmet_id}))
        return claass_list
    except Exception as e:
        print(f"Помилка пошуку класів для предмету: {e}")
        return []

def ob2_ob3(claass_id=1):
    try:
        claass = collection_claass.find_one({'id': claass_id})
        tema_test_list = list(collection_tema_test.find({'claass_id': claass_id}))
        return tema_test_list
    except Exception as e:
        print(f"Помилка пошуку тем тестів для класу: {e}")
        return []

def find_last_Tema_test():
    try:
        return collection_tema_test.find().sort('id', -1).limit(1)
    except Exception as e:
        print(f"Помилка пошуку останньої теми тесту: {e}")
        return None

def find_claass(claass_id):
    try:
        return collection_claass.find_one({'id': claass_id})
    except Exception as e:
        print(f"Помилка пошуку класу: {e}")
        return None

def find_Tema_test_by_id(tema_test_id):
    try:
        return collection_tema_test.find_one({'id': tema_test_id})
    except Exception as e:
        print(f"Помилка пошуку теми тесту: {e}")
        return None

def find_temi_by_predmet(predmet_id):
    try:
        claass_list = ob1_ob2(predmet_id)
        claass_ids = [claass['id'] for claass in claass_list]
        tema_tests = collection_tema_test.find({'claass_id': {'$in': claass_ids}})
        return list(tema_tests)
    except Exception as e:
        print(f"Помилка пошуку тем тестів за предметом: {e}")
        return []

def find_temi_by_test(tema_test_id):
    try:
        tests = list(collection_tests.find({'tema_test_id': tema_test_id}))
        return tests
    except Exception as e:
        print(f"Помилка пошуку тестів за темою тесту: {e}")
        return []

def find_test_to_slovo(slovo):
    try:
        mass = []
        m_slovo = [word[:-2].lower() if len(word) > 3 else word for word in slovo.split()]
        tema_tests = collection_tema_test.find()
        for tema in tema_tests:
            m_text = [word[:-2].lower() if len(word) > 3 else word for word in tema['test_name'].split()]
            fl = False
            for i in m_slovo:
                if (len(i) < 4) or (i in m_text):
                    fl = True
                else:
                    fl = False
                    break
            if fl:
                mass.append(tema)
        return mass
    except Exception as e:
        print(f"Помилка пошуку тем тестів за словом: {e}")
        return []

def mass_ans(tema_test_id):
    try:
        tests = find_temi_by_test(tema_test_id)
        ans_data = [test['ans_data'].replace("\n", "").replace('\r', '').replace('\xa0', '').split('!') for test in tests]
        return ans_data
    except Exception as e:
        print(f"Помилка отримання масиву відповідей: {e}")
        return []

def tes_ans(test_id):
    try:
        test = collection_tests.find_one({'id': test_id})
        ans_data = test['ans_data'].replace("\n", "").replace('\r', '').replace('\xa0', '').split('!')
        return ans_data
    except Exception as e:
        print(f"Помилка отримання відповідей тесту: {e}")
        return []

def find_test(test_id):
    try:
        return collection_tests.find_one({'id': test_id})
    except Exception as e:
        print(f"Помилка пошуку тесту: {e}")
        return None

def first_tema_test(tema_test_id):
    try:
        return collection_tests.find_one({'tema_test_id': tema_test_id})
    except Exception as e:
        print(f"Помилка пошуку першого тесту в темі тесту: {e}")
        return None
def add_test(num_quest, quest_img, quest_text, ans_data, vidpov, tema_test_id):
    try:
        test_data = {
            'num_quest': num_quest,
            'quest_img': quest_img,
            'quest_text': quest_text,
            'ans_data': ans_data,
            'vidpov': vidpov,
            'tema_test_id': tema_test_id
        }
        result = collection_tests.insert_one(test_data)
        tema_test = collection_tema_test.find_one({'id': tema_test_id})
        if tema_test:
            collection_tema_test.update_one(
                {'id': tema_test_id},
                {'$push': {'test_list': result.inserted_id}}
            )
        return result.inserted_id
    except Exception as e:
        print(f"Помилка додавання тесту: {e}")
        return None

def update_test(test_id, num_quest, quest_img, quest_text, ans_data, vidpov):
    try:
        update_data = {
            'num_quest': num_quest,
            'quest_img': quest_img,
            'quest_text': quest_text,
            'ans_data': ans_data,
            'vidpov': vidpov
        }
        result = collection_tests.update_one({'id': test_id}, {'$set': update_data})
        return result.modified_count > 0
    except Exception as e:
        print(f"Помилка оновлення тесту: {e}")
        return False

def update_by_id(collection, id_, update_data):
    try:
        result = collection.update_one({'id': id_}, {'$set': update_data})
        return result.modified_count > 0
    except Exception as e:
        print(f"Помилка оновлення запису: {e}")
        return False

def delete_by_id(collection, id_):
    try:
        result = collection.delete_one({'id': id_})
        return result.deleted_count > 0
    except Exception as e:
        print(f"Помилка видалення запису: {e}")
        return False

def find_by_id(collection, id_):
    try:
        return collection.find_one({'id': id_})
    except Exception as e:
        print(f"Помилка пошуку запису: {e}")
        return None

def get_all_items(collection):
    try:
        return list(collection.find())
    except Exception as e:
        print(f"Помилка отримання всіх записів: {e}")
        return []

def delete_tema_test_and_tests(tema_test_id):
    try:
        # Видалення тестів, пов'язаних з темою тесту
        collection_tests.delete_many({'tema_test_id': tema_test_id})
        # Видалення теми тесту
        collection_tema_test.delete_one({'id': tema_test_id})
    except Exception as e:
        print(f"Помилка видалення теми тесту і тестів: {e}")

def update_test_num_quest(test_id, num_quest):
    try:
        result = collection_tests.update_one({'id': test_id}, {'$set': {'num_quest': num_quest}})
        return result.modified_count > 0
    except Exception as e:
        print(f"Помилка оновлення номера питання тесту: {e}")
        return False

def find_last_test():
    try:
        return list(collection_tests.find().sort('num_quest', -1).limit(1))
    except Exception as e:
        print(f"Помилка пошуку останнього тесту: {e}")
        return []

def min_max_test_id(tema_test_id):
    try:
        test_ids = [test['id'] for test in collection_tests.find({'tema_test_id': tema_test_id})]
        return test_ids
    except Exception as e:
        print(f"Помилка пошуку ідентифікаторів тестів: {e}")
        return []

def jopa():
    pass