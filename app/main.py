from fastapi import FastAPI
from . import  models
from .database import engine
from  .routers import members


app = FastAPI()


models.Base.metadata.create_all(engine)

app.include_router(members.router)
