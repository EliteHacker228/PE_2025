from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router

app = FastAPI(
    title="Table Detector Service",
    description="Сервис определения таблиц и корректировки поворота сканов документов",
    version="1.0.0"
)

# Разрешить кросс-доменные запросы, если нужно использовать с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или конкретный домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение маршрутов
app.include_router(api_router)

