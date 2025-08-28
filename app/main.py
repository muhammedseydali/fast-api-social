# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Hello, FastAPI on Mac!"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}

from fastapi import FastAPI
from .database import engine
from .models import Base
from app.routes import users, auth, posts

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.routers)
app.include_router(posts.router)