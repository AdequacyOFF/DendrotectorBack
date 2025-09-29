from fastapi import FastAPI
import uvicorn
from api import init_routers
from starlette.middleware.cors import CORSMiddleware

def init_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

def create_app() -> FastAPI:
    app = FastAPI(root_path="/api")
    init_routers(app)
    init_middlewares(app)
    return app


if __name__ == "__main__":
    uvicorn.run("main:create_app", host="0.0.0.0", port=1234, reload=True)




