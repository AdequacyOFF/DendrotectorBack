from fastapi import FastAPI
import os

from api import init_routers

app = FastAPI(root_path="/api")
init_routers(app)

# Создаем необходимые директории
os.makedirs("uploads", exist_ok=True)
os.makedirs("results", exist_ok=True)
os.makedirs("temp", exist_ok=True)





