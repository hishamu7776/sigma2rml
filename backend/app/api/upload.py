from fastapi import APIRouter, UploadFile, File, HTTPException
from app.storage.store import store_uploaded_file

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    try:
        path = store_uploaded_file(file.file, file.filename)
        return {"info": f"Saved to {path}"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))