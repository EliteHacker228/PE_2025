from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException,
    status
)
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router
from app.services.detector import process_image_file
import os  # Добавьте импорт os

app = FastAPI(
    title="Table Detector Service",
    description="Сервис определения таблиц и корректировки поворота сканов",
    version="1.0.0")


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())

    try:
        result_path = process_image_file(temp_path)
        return {
            "status": "success",
            "processed_image": result_path,
            "filename": file.filename
        }
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
