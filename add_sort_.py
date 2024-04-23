
import pymongo
import datetime 
client=pymongo.MongoClient("mongodb+srv://mashmanuc:1WTFCFWcW5gbAYCU@cluster0.vbybi6i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db=client.test
coll=db.users
import sqlite3

# Підключення до SQLite
sqlite_conn = sqlite3.connect('basaSS.db')
cursor = sqlite_conn.cursor()

# Виведення списку таблиць
print("Список таблиць:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
for table in tables:
    print(table[0])

# # Виведення вмісту таблиці Predmet
# print("\nВміст таблиці Predmet:")
# cursor.execute("SELECT * FROM Predmet")
# predmets = cursor.fetchall()
# for predmet in predmets:
#     print(predmet)

# Виведення вмісту таблиці Claass
# print("\nВміст таблиці Claass:")
# cursor.execute("SELECT * FROM Claass")
# claasses = cursor.fetchall()
# for claass in claasses:
#     print(claass)

# Виведення вмісту таблиці Tema_test
# print("\nВміст таблиці Tema_test:")
# cursor.execute("SELECT * FROM Tema_test")
# tema_tests = cursor.fetchall()
# for tema_test in tema_tests:
#     print(tema_test)

# Виведення вмісту таблиці Test
print("\nВміст таблиці Test:")
cursor.execute("SELECT * FROM Tests")
tests = cursor.fetchall()
for test in tests:
    print(test)

# sqlite_conn.close()