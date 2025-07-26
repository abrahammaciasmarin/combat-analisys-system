from pymongo import MongoClient
from app.config.config_loader import load_config

config = load_config()
mongo_config = config["database"]["mongodb"]

def get_connection():
    client = MongoClient(mongo_config["uri"])
    db = client[mongo_config["db_name"]]
    collection = db[mongo_config["collection"]]

    return collection
