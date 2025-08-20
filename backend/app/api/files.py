from fastapi import APIRouter, HTTPException
from app.storage.db import load_db, delete_file_record, get_file_record
import os
import yaml

file_router = APIRouter()

def normalize_path(path):
    """Normalize path to use forward slashes for consistency"""
    return path.replace('\\', '/')

def resolve_path(stored_path):
    """Resolve stored path to actual file system path"""
    # Convert forward slashes back to OS-specific separators for file operations
    if os.name == 'nt':  # Windows
        return stored_path.replace('/', '\\')
    else:  # Unix-like systems
        return stored_path

@file_router.get("/")
def list_files():
    """List all uploaded files with their status"""
    try:
        files = load_db()
        # Add additional file info
        for file_info in files:
            # Resolve the stored path to actual file system path
            actual_path = resolve_path(file_info["path"])
            if os.path.exists(actual_path):
                file_info["exists"] = True
                file_info["size"] = os.path.getsize(actual_path)
            else:
                file_info["exists"] = False
                file_info["size"] = 0
        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load file list: {str(e)}")

@file_router.get("/{filename}")
def view_file(filename: str):
    """View the content of a specific file"""
    if not filename or not filename.strip():
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    record = get_file_record(filename)
    if not record:
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        # Resolve the stored path to actual file system path
        actual_path = resolve_path(record["path"])
        
        # Check if file exists on disk
        if not os.path.exists(actual_path):
            raise HTTPException(status_code=404, detail=f"File not found on disk: {actual_path}")
        
        # Read file content
        with open(actual_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Try to parse as YAML to get metadata
        metadata = {}
        try:
            yaml_content = yaml.safe_load(content)
            if yaml_content:
                metadata = {
                    "title": yaml_content.get("title", ""),
                    "description": yaml_content.get("description", ""),
                    "author": yaml_content.get("author", ""),
                    "date": yaml_content.get("date", ""),
                    "tags": yaml_content.get("tags", []),
                    "logsource": yaml_content.get("logsource", {}),
                    "detection": yaml_content.get("detection", {})
                }
        except yaml.YAMLError:
            # Not valid YAML, return as plain text
            pass
        
        return {
            "filename": filename,
            "title": record.get("title", "Untitled Rule"),
            "translated": record.get("translated", False),
            "rml_path": record.get("rml_path", None),
            "content": content,
            "metadata": metadata,
            "file_size": len(content),
            "path": record["path"],
            "actual_path": actual_path
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read file: {str(e)}")

@file_router.get("/rml/{filename}")
def view_rml_legacy(filename: str):
    """Legacy endpoint for viewing RML translation (matches frontend URL structure)"""
    return view_rml(filename)

@file_router.get("/{filename}/rml")
def view_rml(filename: str):
    """View the RML translation of a file"""
    if not filename or not filename.strip():
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    record = get_file_record(filename)
    if not record or not record.get("translated") or not record.get("rml_path"):
        raise HTTPException(status_code=404, detail="RML file not available")
    
    try:
        # Resolve the stored RML path to actual file system path
        actual_rml_path = resolve_path(record["rml_path"])
        
        # Check if RML file exists
        if not os.path.exists(actual_rml_path):
            raise HTTPException(status_code=404, detail=f"RML file not found on disk: {actual_rml_path}")
        
        with open(actual_rml_path, "r", encoding="utf-8") as f:
            rml_content = f.read()
        
        return {
            "filename": filename,
            "title": record.get("title", "Untitled Rule"),
            "rml": rml_content,
            "rml_path": record["rml_path"],
            "actual_rml_path": actual_rml_path,
            "file_size": len(rml_content)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read RML file: {str(e)}")

@file_router.delete("/{filename}")
def delete_file(filename: str):
    """Delete a file and its associated RML translation"""
    if not filename or not filename.strip():
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    record = get_file_record(filename)
    if not record:
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        deleted_files = []
        
        # Resolve the stored path to actual file system path
        actual_path = resolve_path(record["path"])
        
        # Delete the original file if it exists
        if os.path.exists(actual_path):
            os.remove(actual_path)
            deleted_files.append("original file")
        
        # Delete the RML file if it exists
        if record.get("rml_path"):
            actual_rml_path = resolve_path(record["rml_path"])
            if os.path.exists(actual_rml_path):
                os.remove(actual_rml_path)
                deleted_files.append("RML translation")
        
        # Remove from database
        delete_file_record(filename)
        
        return {
            "message": f"File {filename} deleted successfully",
            "deleted": deleted_files,
            "filename": filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

@file_router.get("/{filename}/info")
def get_file_info(filename: str):
    """Get detailed information about a file"""
    if not filename or not filename.strip():
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    record = get_file_record(filename)
    if not record:
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        file_info = {
            "filename": filename,
            "title": record.get("title", "Untitled Rule"),
            "translated": record.get("translated", False),
            "rml_path": record.get("rml_path", None),
            "path": record["path"]
        }
        
        # Resolve the stored path to actual file system path
        actual_path = resolve_path(record["path"])
        
        # Add file system info
        if os.path.exists(actual_path):
            file_info["exists"] = True
            file_info["size"] = os.path.getsize(actual_path)
            file_info["modified"] = os.path.getmtime(actual_path)
            file_info["actual_path"] = actual_path
        else:
            file_info["exists"] = False
            file_info["size"] = 0
            file_info["modified"] = None
            file_info["actual_path"] = actual_path
        
        # Add RML file info
        if record.get("rml_path"):
            actual_rml_path = resolve_path(record["rml_path"])
            if os.path.exists(actual_rml_path):
                file_info["rml_exists"] = True
                file_info["rml_size"] = os.path.getsize(actual_rml_path)
                file_info["rml_modified"] = os.path.getmtime(actual_rml_path)
                file_info["actual_rml_path"] = actual_rml_path
            else:
                file_info["rml_exists"] = False
                file_info["rml_size"] = 0
                file_info["rml_modified"] = None
                file_info["actual_rml_path"] = actual_rml_path
        
        return file_info
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get file info: {str(e)}")