from fastapi.responses import FileResponse, JSONResponse
from fastapi import UploadFile, File, HTTPException, BackgroundTasks, APIRouter
import uuid
from datetime import datetime
from api.schemas import (TaskCreateRequest, TaskCreateResponse,
                         TaskAddMetadataRequest, TaskAddMetadataResponse,
                         TaskStatusRequest, TaskStatusResponse,
                         TaskResultRequest, TaskResultResponse)


router = APIRouter(prefix="/task", tags=["tasks"])


@router.post("/create")
async def upload_image(cmd: TaskCreateRequest, background_tasks: BackgroundTasks):
    """Загрузка изображения для обработки"""
    # Валидация
    if not cmd.file.content_type.startswith('image/'):
        raise HTTPException(400, "File must be an image")

    # Генерируем task_id
    task_id = str(uuid.uuid4())

    # Сохраняем файл
    content = await cmd.file.read()
    file_extension = cmd.file.filename.split('.')[-1] if '.' in cmd.file.filename else 'jpg'
    file_path = f"uploads/{task_id}.{file_extension}"

    with open(file_path, "wb") as f:
        f.write(content)

    # Инициализируем задачу
    tasks_storage[task_id] = {
        "status": "processing",
        "original_filename": cmd.file.filename,
        "file_size": len(content),
        "uploaded_at": datetime.now().isoformat(),
        "progress": 0
    }

    # Запускаем обработку в фоне
    background_tasks.add_task(simulate_ai_processing, task_id, file_path)

    TaskCreateResponse(
        task_id=task_id,
        task_status=task_status,
    )
    return TaskCreateResponse


# Эндпоинт для получения информации о файле без скачивания
@router.get("/add_metadata")
async def get_file_info(cmd: TaskAddMetadataRequest):
    """Получение информации о результате без скачивания"""
    if cmd.task_id not in tasks_storage:
        raise HTTPException(404, "Task not found")

    task_data = tasks_storage[cmd.task_id]

    if task_data["status"] != "completed":
        raise HTTPException(425, "Result is not ready yet")

    zip_path = task_data["zip_path"]

    return TaskAddMetadataResponse


@router.get("/status")
async def get_status(cmd: TaskStatusRequest):
    """Проверка статуса обработки"""
    if cmd.task_id not in tasks_storage:
        raise HTTPException(404, "Task not found")

    task_data = tasks_storage[cmd.task_id].copy()

    # Возвращаем соответствующие данные в зависимости от статуса
    if task_data["status"] == "completed":
        response_data = {
            "task_id": cmd.task_id,
            "status": "completed",
            "download_url": f"/api/download/{cmd.task_id}",
            "file_size": task_data.get("file_size"),
            "completed_at": task_data.get("completed_at")
        }
    elif task_data["status"] == "processing":
        response_data = {
            "task_id": cmd.task_id,
            "status": "processing",
            "progress": task_data.get("progress", 0),
            "message": "AI is processing your image"
        }
    else:  # error
        response_data = {
            "task_id": cmd.task_id,
            "status": "error",
            "error": task_data.get("error", "Unknown error")
        }

    return TaskStatusResponse


@router.get("/result")
async def download_result(cmd: TaskResultRequest):
    """Скачивание результата"""
    if cmd.task_id not in tasks_storage:
        raise HTTPException(404, "Task not found")

    task_data = tasks_storage[cmd.task_id]

    if task_data["status"] != "completed":
        raise HTTPException(425, "Result is not ready yet")

    zip_path = task_data["zip_path"]

    if not os.path.exists(zip_path):
        raise HTTPException(404, "Result file not found")

    # Генерируем читаемое имя файла
    original_name = task_data.get("original_filename", "image")
    base_name = os.path.splitext(original_name)[0]
    download_filename = f"AI_Analysis_{base_name}_{cmd.task_id[:8]}.zip"
    response = TaskResultResponse(path=zip_path,
                                  filename=download_filename,
                                  media_type="application/zip",
                                  headers={
                                    "X-Task-ID": cmd.task_id,
                                    "X-File-Size": str(os.path.getsize(zip_path)),
                                    "Content-Disposition": f"attachment; filename={download_filename}"
                                    }
                                  )
    return response


