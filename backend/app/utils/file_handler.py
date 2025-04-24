import shutil
from fastapi import UploadFile

async def save_uploaded_file(file: UploadFile) -> str:
    file_location = f"uploaded_{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    return file_location