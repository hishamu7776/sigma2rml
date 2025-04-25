from fastapi import APIRouter, HTTPException
from app.storage.db import load_db, delete_file_record, get_file_record
import os

file_router = APIRouter()

@file_router.get("/")
def list_files():
    return load_db()

@file_router.get("/{filename}")
def view_file(filename: str):
    record = get_file_record(filename)
    if not record:
        raise HTTPException(status_code=404, detail="File not found")
    with open(record["path"], "r") as f:
        return {"filename": filename, "content": f.read()}

@file_router.get("/rml/{filename}")
def view_rml(filename: str):
    record = get_file_record(filename)
    if not record or not record.get("translated") or not record.get("rml_path"):
        raise HTTPException(status_code=404, detail="RML file not available")
    with open(record["rml_path"], "r") as f:
        return {"filename": filename, "rml": f.read()}

@file_router.delete("/{filename}")
def delete_file(filename: str):
    record = get_file_record(filename)
    if not record:
        raise HTTPException(status_code=404, detail="File not found")
    os.remove(record["path"])
    delete_file_record(filename)
    return {"message": f"File {filename} deleted"}