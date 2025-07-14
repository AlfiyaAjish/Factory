
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId

load_dotenv()


MONGO_URI = os.getenv("MONGO_URI")


if not MONGO_URI:
    raise ValueError(" MONGO_URI is not set in the .env file")

try:
    #  Initialize MongoDB client
    client = MongoClient(MONGO_URI)


    client.admin.command('ping')
    print(" Connected to MongoDB Atlas")
    db = client["smart_factory"]
    machines_collection = db["machines"]
    metrics_collection = db["metrics"]
    alerts_collection = db["alerts"]
    reports_collection = db["reports"]
    users_collection = db["users"]
    ownership_collection=db["ownership"]


except ConnectionFailure as e:
    print(" MongoDB connection failed:", str(e))
    raise e


def is_machine_registered(machine_id: str) -> bool:
    return machines_collection.find_one({"machine_id": machine_id}) is not None

def register_machine(machine: dict):
    if not is_machine_registered(machine["machine_id"]):
        machines_collection.insert_one(machine)



def clean_mongo_id(doc):
    if "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])
    return doc