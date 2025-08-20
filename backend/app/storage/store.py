import os
from app.storage.db import add_file_record
import yaml

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def normalize_path(path):
    """Normalize path to use forward slashes for consistency"""
    return path.replace('\\', '/')

def store_uploaded_file(file, filename):
    """Store an uploaded file and register it in the database"""
    try:
        # Validate filename
        if not filename or not filename.strip():
            raise ValueError("Invalid filename")
        
        # Check for path traversal attempts
        if '..' in filename or '/' in filename or '\\' in filename:
            raise ValueError("Invalid filename - path traversal not allowed")
        
        # Create safe filename
        safe_filename = os.path.basename(filename)
        path = os.path.join(UPLOAD_DIR, safe_filename)
        
        # Normalize path for consistent storage
        normalized_path = normalize_path(path)
        
        # Check if file already exists
        if os.path.exists(path):
            raise ValueError(f"A file with the name '{safe_filename}' already exists")
        
        # Read file content
        file.seek(0)  # Reset file pointer
        content = file.read()
        
        # Validate file content
        if not content:
            raise ValueError("File is empty")
        
        # Check file size (limit to 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if len(content) > max_size:
            raise ValueError(f"File too large. Maximum size: {max_size // (1024*1024)}MB")
        
        # Save file
        with open(path, "wb") as f:
            f.write(content)
        
        # Try to extract YAML title and validate format
        title = ""
        try:
            # Reset file pointer for reading
            file.seek(0)
            yaml_content = yaml.safe_load(file)
            
            if yaml_content:
                title = yaml_content.get("title", "")
                
                # Basic validation of Sigma rule structure
                if "detection" not in yaml_content:
                    raise ValueError("File does not appear to be a valid Sigma rule (missing 'detection' section)")
                
                detection = yaml_content.get("detection", {})
                if not detection or "condition" not in detection:
                    raise ValueError("File does not appear to be a valid Sigma rule (missing 'condition' in detection)")
                    
        except yaml.YAMLError:
            # Not valid YAML, but we'll still store it
            title = ""
        except ValueError as ve:
            # Sigma rule validation failed
            raise ValueError(f"Sigma rule validation failed: {str(ve)}")
        
        # Register in database with normalized path
        add_file_record(safe_filename, normalized_path, title)
        
        return normalized_path
        
    except Exception as e:
        # Clean up any partially created files
        if 'path' in locals() and os.path.exists(path):
            try:
                os.remove(path)
            except:
                pass
        raise e

def get_file_info(filepath):
    """Get information about a stored file"""
    try:
        # Normalize path for consistency
        normalized_path = normalize_path(filepath)
        
        if not os.path.exists(normalized_path):
            return None
        
        file_info = {
            "path": normalized_path,
            "filename": os.path.basename(normalized_path),
            "size": os.path.getsize(normalized_path),
            "modified": os.path.getmtime(normalized_path),
            "exists": True
        }
        
        # Try to get YAML metadata
        try:
            with open(normalized_path, 'r', encoding='utf-8') as f:
                content = f.read()
                yaml_content = yaml.safe_load(content)
                
                if yaml_content:
                    file_info["metadata"] = {
                        "title": yaml_content.get("title", ""),
                        "description": yaml_content.get("description", ""),
                        "author": yaml_content.get("author", ""),
                        "date": yaml_content.get("date", ""),
                        "tags": yaml_content.get("tags", []),
                        "logsource": yaml_content.get("logsource", {}),
                        "detection": yaml_content.get("detection", {})
                    }
        except:
            file_info["metadata"] = None
        
        return file_info
        
    except Exception as e:
        return None

