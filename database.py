from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["it_staffing"]
collection = db["candidates"]

def store_candidate(data):
    collection.insert_one(data)