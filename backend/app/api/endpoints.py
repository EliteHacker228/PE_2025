import shutil
import uuid
import os
from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse
from app.services.detector import process_image_file

router = APIRouter()


@router.post("/upload", response_class=FileResponse)  # Убедитесь что это FileResponse
async def upload_file(
        file: UploadFile = File(...),
        background_tasks: BackgroundTasks = BackgroundTasks()
):
    try:
        # Сохраняем временный файл
        temp_filename = f"temp_{uuid.uuid4().hex}.jpg"
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Обрабатываем файл (должен вернуть путь к обработанному файлу)
        output_path = process_image_file(temp_filename)

        if not os.path.exists(output_path):
            raise HTTPException(500, "Output file was not created")

        # Удаление временных файлов после отправки
        background_tasks.add_task(os.remove, temp_filename)
        background_tasks.add_task(os.remove, output_path)

        # Возвращаем файл
        return FileResponse(
            output_path,
            media_type="image/jpeg",
            filename="processed_image.jpg"
        )
    except Exception as e:
        # Очистка при ошибке
        if 'temp_filename' in locals() and os.path.exists(temp_filename):
            os.remove(temp_filename)
        if 'output_path' in locals() and os.path.exists(output_path):
            os.remove(output_path)
        raise HTTPException(500, str(e))
