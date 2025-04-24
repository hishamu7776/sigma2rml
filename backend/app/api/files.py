from fastapi import APIRouter, HTTPException
from app.storage.db import load_db, delete_file_record, get_file_record
import os

router = APIRouter()

@router.get("/")
def list_files():
    return load_db()

@router.get("/{filename}")
def view_file(filename: str):
    record = get_file_record(filename)
    if not record:
        raise HTTPException(status_code=404, detail="File not found")
    with open(record["path"], "r") as f:
        return {"filename": filename, "content": f.read()}

@router.delete("/{filename}")
def delete_file(filename: str):
    record = get_file_record(filename)
    if not record:
        raise HTTPException(status_code=404, detail="File not found")
    os.remove(record["path"])
    delete_file_record(filename)
    return {"message": f"File {filename} deleted"}
