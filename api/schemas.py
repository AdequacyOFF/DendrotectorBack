from pydantic import BaseModel, Field
from fastapi import File
from uuid import UUID
from fastapi.responses import FileResponse


class TaskCreateRequest(BaseModel):
    file: File = Field(description="Картинка для распознавания")


class TaskCreateResponse(BaseModel):
    task_id: UUID = Field(description="Id запроса")
    task_status: str = Field(description="Статус запроса")


class TaskAddMetadataRequest(BaseModel):
    task_id: UUID = Field(description="Id запроса")
    task_comment: str = Field(description="Комментарий к задаче")
    task_geo: (float, float) = Field(description="Координаты к задаче")


class TaskAddMetadataResponse(BaseModel):
    task_id: UUID = Field(description="Id запроса")
    task_status: str = Field(description="Статус запроса")


class TaskStatusRequest(BaseModel):
    task_id: UUID = Field(description="Id запроса")


class TaskStatusResponse(BaseModel):
    task_id: UUID = Field(description="Id запроса")
    task_status: str = Field(description="Статус запроса")


class TaskResultRequest(BaseModel):
    task_id: UUID = Field(description="Id запроса")


class TaskResultResponse(FileResponse):
    path: str = Field(description="Путь к архиву")
    filename: str = Field(description="Имя архива у клиента")
    media_type: str = "application/zip",
    headers = {
        "X-Task-ID": UUID,
        "X-File-Size": str,
        "Content-Disposition": str,
    }


