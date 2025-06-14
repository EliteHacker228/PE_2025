from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

from app.api.endpoints import router as api_router
from app.services.detector import process_image_file


app = FastAPI(
    title="Table Detector Service",
    description="Сервис определения таблиц и корректировки поворота сканов",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
