from fastapi import FastAPI

from app.db.session import Base, engine
import app.db.models.models  
from app.api.routers import auth as auth_router
from app.api.routers import users as users_router  

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router.router) 
app.include_router(users_router.router)

@app.get("/")
def test() -> dict[str, str]:
    return {"status": "ok"}
