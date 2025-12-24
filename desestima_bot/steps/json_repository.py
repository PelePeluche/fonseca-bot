# File: json_repository.py

import json
import os

def load_database(db_path):
    if os.path.exists(db_path):
        with open(db_path, 'r') as file:
            return json.load(file)
    else:
        return {"success": [], "errors": []}

def save_database(db_path, data):
    with open(db_path, 'w') as file:
        json.dump(data, file, indent=4)

def log_success(db_path, case_number, message):
    data = load_database(db_path)
    data["success"].append({"case_number": case_number, "message": message})
    save_database(db_path, data)

def log_error(db_path, case_number, error_message):
    data = load_database(db_path)
    data["errors"].append({"case_number": case_number, "error": error_message})
    save_database(db_path, data)
