import json
import os

DB_PATH = "file_registry.json"

def load_db():
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as f:
            json.dump([], f)
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2)

def add_file_record(filename, path, title=""):
    db = load_db()
    db.append({"filename": filename, "path": path, "title": title})
    save_db(db)

def delete_file_record(filename):
    db = load_db()
    db = [f for f in db if f["filename"] != filename]
    save_db(db)

def get_file_record(filename):
    return next((f for f in load_db() if f["filename"] == filename), None)