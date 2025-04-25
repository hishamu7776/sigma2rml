from fastapi import FastAPI
from app.api import upload, transpile, files, translate
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or ["*"] for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(transpile.router, prefix="/transpile", tags=["Transpile"])
app.include_router(files.file_router, prefix="/files", tags=["File Management"])
app.include_router(translate.translate_router, prefix="/translate", tags=["Translate"])

@app.get("/")
def root():
    return {"message": "Welcome to Sigma2RML backend"}