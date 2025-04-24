from fastapi import APIRouter, Form, HTTPException
from app.core.transpiler import SigmaToRMLTranspiler

router = APIRouter()
transpiler = SigmaToRMLTranspiler()

@router.post("/")
async def transpile_sigma(sigma_text: str = Form(...)):
    try:
        result = transpiler.transpile(sigma_text)
        return {"rml": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
