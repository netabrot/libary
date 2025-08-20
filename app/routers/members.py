from fastapi import APIRouter
from .. import database, schemas, models
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,status
from ..repository import member

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db

