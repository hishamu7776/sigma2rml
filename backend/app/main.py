from fastapi import FastAPI
from app.api import upload, transpile, files

app = FastAPI()
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(transpile.router, prefix="/transpile", tags=["Transpile"])
app.include_router(files.router, prefix="/files", tags=["File Management"])

@app.get("/")
def root():
    return {"message": "Welcome to Sigma2RML backend"}