import shutil
import uuid
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app.services.detector import process_image_file

router = APIRouter()


@router.post("/detect-rotate/", response_class=FileResponse)
async def detect_and_rotate(file: UploadFile = File(...)):
    temp_filename = f"temp_{uuid.uuid4().hex}.jpg"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_path = process_image_file(temp_filename)

    return FileResponse(output_path, filename="rotated_output.jpg")
