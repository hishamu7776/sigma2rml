from fastapi import APIRouter, UploadFile, File
from app.utils.file_handler import save_uploaded_file

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    location = await save_uploaded_file(file)
    return {"info": f"Saved to {location}"}