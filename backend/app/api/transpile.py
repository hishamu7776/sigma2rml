from fastapi import APIRouter, Form, HTTPException
from app.core.transpiler_refactored import RefactoredTranspiler
import yaml

router = APIRouter()
transpiler = RefactoredTranspiler()

@router.post("/")
async def transpile_sigma(sigma_text: str = Form(...)):
    """Transpile Sigma rule text to RML"""
    try:
        # Validate input
        if not sigma_text or not sigma_text.strip():
            raise HTTPException(status_code=400, detail="Sigma rule text is required")
        
        # Try to parse as YAML first
        try:
            yaml_content = yaml.safe_load(sigma_text)
            if not yaml_content:
                raise HTTPException(status_code=400, detail="Invalid YAML format")
        except yaml.YAMLError as e:
            raise HTTPException(status_code=400, detail=f"Invalid YAML format: {str(e)}")
        
        # Transpile to RML
        result = transpiler.transpile(sigma_text)
        
        if not result:
            raise HTTPException(status_code=500, detail="Transpilation failed - no output generated")
        
        return {
            "status": "success",
            "rml": result,
            "input_length": len(sigma_text),
            "output_length": len(result),
            "message": "Sigma rule successfully transpiled to RML"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transpilation failed: {str(e)}")

@router.post("/validate")
async def validate_sigma(sigma_text: str = Form(...)):
    """Validate Sigma rule format without transpiling"""
    try:
        # Validate input
        if not sigma_text or not sigma_text.strip():
            raise HTTPException(status_code=400, detail="Sigma rule text is required")
        
        # Try to parse as YAML
        try:
            yaml_content = yaml.safe_load(sigma_text)
            if not yaml_content:
                raise HTTPException(status_code=400, detail="Invalid YAML format")
        except yaml.YAMLError as e:
            raise HTTPException(status_code=400, detail=f"Invalid YAML format: {str(e)}")
        
        # Check for required fields
        required_fields = ['detection']
        missing_fields = [field for field in required_fields if field not in yaml_content]
        
        if missing_fields:
            raise HTTPException(
                status_code=400, 
                detail=f"Missing required fields: {', '.join(missing_fields)}"
            )
        
        # Check detection structure
        detection = yaml_content.get('detection', {})
        if not detection:
            raise HTTPException(status_code=400, detail="Detection section is empty")
        
        # Check for at least one condition
        if 'condition' not in detection:
            raise HTTPException(status_code=400, detail="No condition specified in detection")
        
        return {
            "status": "success",
            "valid": True,
            "message": "Sigma rule format is valid",
            "structure": {
                "has_title": "title" in yaml_content,
                "has_logsource": "logsource" in yaml_content,
                "has_detection": True,
                "detection_keys": list(detection.keys())
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")
