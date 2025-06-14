import os
import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse

from app.services.detector import process_image_file

router = APIRouter()


@router.post("/detect-rotate/", response_class=FileResponse)
async def upload_file(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    """Endpoint for image processing with automatic rotation detection."""
    temp_filename = f"temp_{uuid.uuid4().hex}.jpg"
    output_path = None

    try:
        # Save temporary file
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        output_path = process_image_file(temp_filename)

        if not Path(output_path).exists():
            raise HTTPException(
                status_code=500,
                detail="Output file was not created"
            )

        background_tasks.add_task(cleanup, temp_filename, output_path)

        return FileResponse(
            output_path,
            media_type="image/jpeg",
            filename="processed_image.jpg"
        )

    except HTTPException:
        raise
    except Exception as e:
        cleanup(temp_filename, output_path)
        raise HTTPException(
            status_code=500,
            detail=f"Image processing failed: {str(e)}"
        ) from e


def cleanup(*file_paths):
    """Clean up temporary files."""
    for path in file_paths:
        if path and Path(path).exists():
            try:
                Path(path).unlink()
            except OSError as e:
                print(f"Error deleting file {path}: {e}")
