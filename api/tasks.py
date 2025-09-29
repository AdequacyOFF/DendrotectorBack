from fastapi.responses import FileResponse
from fastapi import UploadFile, File, HTTPException, BackgroundTasks, APIRouter
from datetime import datetime
import os

router = APIRouter(prefix="/task", tags=["tasks"])

tasks_storage = {}


@router.post("/generate")
async def upload_image(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Загрузка изображения для обработки"""

    # Валидация
    if not file.content_type.startswith('image/'):
        raise HTTPException(400, "File must be an image")
    generation_start_time = datetime.now().date()

    # Создаем необходимые директории, если их нет
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    # Сохраняем файл
    content = await file.read()
    file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
    file_path = f"uploads/{generation_start_time}.{file_extension}"

    with open(file_path, "wb") as f:
        f.write(content)

    original_filename = file.filename

    #
    # где-то здесь жоска генерим
    #
    # путь к сгенерированному архиву
    zip_path = "results/report.zip"

    if not os.path.exists(zip_path):
        raise HTTPException(404, "Result file not found")

    def file_generator():
        with open(zip_path, "rb") as f:
            while chunk := f.read(8192):
                yield chunk

    return FileResponse(
        path=zip_path,
        filename=f"{original_filename}.zip",
        media_type="application/zip"
    )





