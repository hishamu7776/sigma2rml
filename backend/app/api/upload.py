from fastapi import APIRouter, UploadFile, File, HTTPException
from app.storage.store import store_uploaded_file
import os

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    """Upload a Sigma rule file"""
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        # Check file extension
        allowed_extensions = ['.yml', '.yaml', '.rml']
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
            )
        
        # Check file size (limit to 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if file.size and file.size > max_size:
            raise HTTPException(
                status_code=400, 
                detail=f"File too large. Maximum size: {max_size // (1024*1024)}MB"
            )
        
        # Store the file
        path = store_uploaded_file(file.file, file.filename)
        
        return {
            "status": "success",
            "filename": file.filename,
            "path": path,
            "message": f"File {file.filename} uploaded successfully"
        }
        
    except HTTPException:
        raise
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/allowed-types")
def get_allowed_file_types():
    """Get list of allowed file types for upload"""
    return {
        "allowed_extensions": ['.yml', '.yaml', '.rml'],
        "max_file_size_mb": 10,
        "description": "Sigma rule files (YAML) and RML files"
    }