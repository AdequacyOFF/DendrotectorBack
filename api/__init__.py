from fastapi import FastAPI

from api.tasks import router as task_router


def init_routers(app: FastAPI):
    app.include_router(task_router)