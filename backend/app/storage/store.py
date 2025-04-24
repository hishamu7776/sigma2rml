import os
from app.storage.db import add_file_record
import yaml

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def store_uploaded_file(file, filename):
    path = os.path.join(UPLOAD_DIR, filename)

    # Save file
    with open(path, "wb+") as f:
        f.write(file.read())

    # Try to extract YAML title
    try:
        with open(path, 'r') as yf:
            content = yaml.safe_load(yf)
        title = content.get("title", "")
    except:
        title = ""

    # Attempt to register in database
    add_file_record(filename, path, title)
    return path

