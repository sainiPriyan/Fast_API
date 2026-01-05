from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user, login

app = FastAPI()

app.include_router(user.router)
app.include_router(login.router)

models.Base.metadata.create_all(bind=engine)