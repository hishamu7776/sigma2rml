from fastapi import APIRouter, HTTPException
from app.core.transpiler import SigmaToRMLTranspiler
from app.storage.db import get_file_record, update_translation_status
import os
import yaml

router = APIRouter()
transpiler = SigmaToRMLTranspiler()

def resolve_path(stored_path):
    """Resolve stored path to actual file system path"""
    # Convert forward slashes back to OS-specific separators for file operations
    if os.name == 'nt':  # Windows
        return stored_path.replace('/', '\\')
    else:  # Unix-like systems
        return stored_path

@router.post("/{filename}")
def translate_sigma_file(filename: str):
    """Translate a Sigma rule file to RML"""
    # Validate filename
    if not filename or not filename.strip():
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    # Get file record
    record = get_file_record(filename)
    if not record:
        raise HTTPException(status_code=404, detail="File not found")

    try:
        # Resolve the stored path to actual file system path
        actual_path = resolve_path(record["path"])
        
        # Check if file exists on disk
        if not os.path.exists(actual_path):
            raise HTTPException(status_code=404, detail=f"File not found on disk: {actual_path}")
        
        # Read and validate Sigma rule
        with open(actual_path, "r", encoding="utf-8") as f:
            sigma_text = f.read()
        
        if not sigma_text.strip():
            raise HTTPException(status_code=400, detail="File is empty")
        
        # Validate YAML format
        try:
            yaml_content = yaml.safe_load(sigma_text)
            if not yaml_content:
                raise HTTPException(status_code=400, detail="Invalid YAML format")
        except yaml.YAMLError as e:
            raise HTTPException(status_code=400, detail=f"Invalid YAML format: {str(e)}")
        
        # Transpile to RML
        rml_output = transpiler.transpile(sigma_text)
        
        if not rml_output:
            raise HTTPException(status_code=500, detail="Transpilation failed - no output generated")
        
        # Create translated_files directory if it doesn't exist
        translated_dir = "translated_files"
        os.makedirs(translated_dir, exist_ok=True)
        
        # Save translated RML to file
        rml_filename = filename.rsplit('.', 1)[0] + ".rml"
        rml_path = os.path.join(translated_dir, rml_filename)
        
        # Normalize path for storage (use forward slashes)
        normalized_rml_path = rml_path.replace('\\', '/')
        
        with open(rml_path, "w", encoding="utf-8") as f:
            f.write(rml_output)

        # Update database record with normalized path
        update_translation_status(filename, normalized_rml_path)
        
        return {
            "status": "success", 
            "filename": filename,
            "rml_text": rml_output,
            "rml_path": normalized_rml_path,
            "actual_rml_path": rml_path,
            "message": f"Successfully translated {filename} to RML"
        }

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error for debugging
        print(f"Error translating {filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@router.get("/{filename}/status")
def get_translation_status(filename: str):
    """Get the translation status of a file"""
    record = get_file_record(filename)
    if not record:
        raise HTTPException(status_code=404, detail="File not found")
    
    return {
        "filename": filename,
        "translated": record.get("translated", False),
        "rml_path": record.get("rml_path", None),
        "title": record.get("title", "Untitled")
    }
