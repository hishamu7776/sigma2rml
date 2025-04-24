from fastapi import APIRouter, UploadFile, File
from app.storage.store import store_uploaded_file

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    path = store_uploaded_file(file.file, file.filename)
    return {"info": f"Saved to {path}"}