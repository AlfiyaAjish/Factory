from scripts.utils.mongodb_utils import machines_collection

def get_all_machines():
    return list(machines_collection.find({}, {"_id": 0}))

def get_machines_by_line(line_name):
    return list(machines_collection.find({"line": line_name}, {"_id": 0}))

def get_machines_by_operator(operator_name):
    return list(machines_collection.find({"operator": operator_name}, {"_id": 0}))
