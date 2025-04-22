from fastapi import FastAPI, UploadFile, File
import shutil
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Sigma2RML backend"}

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"uploaded_{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}
