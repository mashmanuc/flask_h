from flask import flash
from passlib.hash import sha256_crypt
from datetime import datetime
from flask_login import UserMixin
from pymongo import MongoClient, errors
from config import MONGO_KEY


# Підключення до MongoDB

client = MongoClient(MONGO_KEY)
db = client['users']
users_collection = db['users']
user_test_collection = db['user_test']

# class User(UserMixin):
#     def __init__(self, username, email, password):
#         self.username = username
#         self.email = email
#         self.password = sha256_crypt.encrypt(password)

#     def checkPassword(self, entered_password):
#         return sha256_crypt.verify(entered_password, self.password)

#     def get_id(self):
#         return str(self.id)

#     @staticmethod
#     def get_user_by_username(username):
#         user = users_collection.find_one({"username": username})
#         return user

#     @staticmethod
#     def add_user_to_database(username, email, password):
#         try:
#             new_user = {
#                 "username": username,
#                 "email": email,
#                 "password": sha256_crypt.encrypt(password)
#             }
#             users_collection.insert_one(new_user)
#             flash('Тепер ви зареєстровані та можете увійти!', 'success')
#             return True
#         except Exception as e:
#             flash('Error: User already exists.')
#             return False
from passlib.hash import sha256_crypt  # Assuming SHA-256 for now (consider bcrypt)

class User(UserMixin):
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = sha256_crypt.encrypt(password)

    def checkPassword(self, entered_password):
        return sha256_crypt.verify(entered_password, self.password)

    def get_id(self):
        # Replace with the appropriate unique identifier field
        return self.username  # Example (adjust based on your data model)

    @staticmethod
    def get_user_by_username(username, users_collection):  # Explicitly pass collection
        user = users_collection.find_one({"username": username})
        return user

    @staticmethod
    def add_user_to_database(username, email, password, users_collection):
        try:
            new_user = {
                "username": username,
                "email": email,
                "password": sha256_crypt.encrypt(password)
            }
            users_collection.insert_one(new_user)
            return True
        except errors.DuplicateKeyError as e:
            # Handle duplicate username error more specifically
            return False
        except Exception as e:
            # Handle other potential errors
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