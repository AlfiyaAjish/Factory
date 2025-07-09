from scripts.utils.mongodb_utils import machines_collection

def get_all_machines():
    return list(machines_collection.find({}, {"_id": 0}))
