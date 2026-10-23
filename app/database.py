import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongodb_url = os.getenv("MONGODB_URL")
database_name = os.getenv("MONGODB_DATABASE", "food_delivery")

client = MongoClient(mongodb_url)
db = client[database_name]

menu_items_collection = db["menu_items"]
