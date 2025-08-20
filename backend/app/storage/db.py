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
    # Validate inputs
    if not filename or not filename.strip():
        raise ValueError("Filename cannot be empty")
    if not path or not path.strip():
        raise ValueError("File path cannot be empty")
    
    db = load_db()
    # Enforce uniqueness
    if any(f["filename"] == filename for f in db):
        raise ValueError("A file with this filename already exists.")
    if any(f["title"] == title for f in db if title):
        raise ValueError("A file with this title already exists.")
    db.append({
        "filename": filename,
        "path": path,
        "title": title,
        "translated": False,
        "rml_path": None
    })
    save_db(db)

def delete_file_record(filename):
    if not filename or not filename.strip():
        raise ValueError("Filename cannot be empty")
        
    db = load_db()
    db = [f for f in db if f["filename"] != filename]
    save_db(db)

def get_file_record(filename):
    if not filename or not filename.strip():
        return None
        
    return next((f for f in load_db() if f["filename"] == filename), None)

def update_translation_status(filename, rml_path):
    if not filename or not filename.strip():
        raise ValueError("Filename cannot be empty")
    if not rml_path or not rml_path.strip():
        raise ValueError("RML path cannot be empty")
        
    db = load_db()
    for f in db:
        if f["filename"] == filename:
            f["translated"] = True
            f["rml_path"] = rml_path
            break
    save_db(db)
