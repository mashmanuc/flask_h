import bcrypt
from datetime import datetime
from pymongo import MongoClient, errors
from config import MONGO_KEY

client = MongoClient(MONGO_KEY)
db = client['users']
users_collection = db['users']
user_test_collection = db['user_test']

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password  # Використовуємо вже закодований пароль

    def checkPassword(self, entered_password):
        return bcrypt.checkpw(entered_password.encode('utf-8'), self.password)


    @staticmethod
    def get_user_by_username(username, users_collection):
        return users_collection.find_one({"username": username})

    @classmethod
    def add_user_to_database(cls, username, email, password, users_collection):
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            new_user = {
                "username": username,
                "email": email,
                "password": hashed_password
            }
            users_collection.insert_one(new_user)
            return True
        except errors.DuplicateKeyError as e:
            return False
        except Exception as e:
            return False

def add_user_test(users_id, num_quest, tema_test_id, test_id, vid, pr_vid):
    existing_record = user_test_collection.find_one({"users_id": users_id, "test_id": test_id})

    if existing_record:
        user_test_collection.update_one(
            {"users_id": users_id, "test_id": test_id},
            {"$set": {"vid": vid, "pr_vid": pr_vid}}
        )
    else:
        new_user_test = {
            "users_id": users_id,
            "num_quest": num_quest,
            "tema_test_id": tema_test_id,
            "test_id": test_id,
            "vid": vid,
            "pr_vid": pr_vid,
            "date_completed": datetime.utcnow()
        }
        user_test_collection.insert_one(new_user_test)

def user_test(users_id, tema_test_id):
    records = list(user_test_collection.find({"users_id": users_id, "tema_test_id": tema_test_id}))
    return [(record["test_id"], record["vid"], record["num_quest"].split()[-1]) for record in records]

def user_res_test(users_id, tema_test_id):
    return list(user_test_collection.find({"users_id": users_id, "tema_test_id": tema_test_id}, {"_id": 0}).sort("test_id", 1))

def dinamic(users_id, tema_test_id):
    records = list(user_test_collection.find({"users_id": users_id, "tema_test_id": tema_test_id}))
    return [record["test_id"] for record in records]

def user_t_ans(users_id, tema_test_id):
    records = list(user_test_collection.find({"users_id": users_id, "tema_test_id": tema_test_id}, {"test_id": 1, "vid": 1, "_id": 0}))
    return [(record["test_id"], record["vid"]) for record in records]

def find_vid(users_id, tema_test_id, test_id):
    user_test_record = user_test_collection.find_one({"users_id": users_id, "tema_test_id": tema_test_id, "test_id": test_id})
    if user_test_record:
        return user_test_record["vid"]
    else:
        return None

def vidsotok(users_id, tema_test_id):
    ress = user_res_test(users_id, tema_test_id)
    summa = 0
    for res in ress:
        len_diff = len(res["vid"]) - len(res["pr_vid"])
        if len_diff > 0:
            res["pr_vid"] = res["pr_vid"].ljust(len(res["vid"]), ' ')
        elif len_diff < 0:
            res["vid"] = res["vid"].ljust(len(res["pr_vid"]), ' ')

        if res["pr_vid"].lower() == res["vid"].lower():
            summa += 1

    vid = round((summa / len(ress)) * 100) if ress else 0
    return vid
