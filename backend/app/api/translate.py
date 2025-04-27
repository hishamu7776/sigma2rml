from fastapi import APIRouter, HTTPException
from app.core.transpiler import SigmaToRMLTranspiler
from app.storage.db import get_file_record, update_translation_status
import os

router = APIRouter()
transpiler = SigmaToRMLTranspiler()

@router.post("/{filename}")
def translate_sigma_file(filename: str):
    record = get_file_record(filename)
    if not record:
        raise HTTPException(status_code=404, detail="File not found")

    try:
        with open(record["path"], "r") as f:
            sigma_text = f.read()
        rml_output = transpiler.transpile(sigma_text)
        # Save translated RML to file (optional)
        rml_filename = filename.rsplit('.', 1)[0] + ".rml"
        rml_path = os.path.join("uploaded_files", rml_filename)
        with open(rml_path, "w") as f:
            f.write(rml_output)

        update_translation_status(filename, rml_path)
        return {"status": "success", "rml_text": rml_output}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
