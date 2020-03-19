# Connection
from pymongo import MongoClient

customer_id = 12345678

cluster = MongoClient(
    "mongodb+srv://mustajabhannan:Hannan786@cluster0-n7aqf.mongodb.net/test?retryWrites=true&w=majority")

db = cluster["dynamic_cv"]
collection = db["users"]

fetch_record = collection.find_one({"cust_id": customer_id})

object_id = fetch_record['_id']
