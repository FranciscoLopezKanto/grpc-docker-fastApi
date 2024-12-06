from pymongo import MongoClient
from bson.objectid import ObjectId

# Configuración MongoDB
MONGO_URI = "mongodb+srv://Admin:L3wOx7kWB3t0GXbs@cluster0.azhio.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["users_db"]
users_collection = db["users"]

def find_user_by_email(email):
    return users_collection.find_one({"email": email})

def find_user_by_id(user_id):
    return users_collection.find_one({"_id": ObjectId(user_id)})

def find_all_users():
    return users_collection.find()

def insert_user(user_data):
    return users_collection.insert_one(user_data)

def update_user(user_id, updated_data):
    return users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_data})

def delete_user(user_id):
    return users_collection.delete_one({"_id": ObjectId(user_id)})
