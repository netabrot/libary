from fastapi import FastAPI

from app.api.deps import ResponseTimeMiddleware
from app.db.session import Base, engine
from app.api.routers import auth as auth_router
from app.api.routers import users as users_router  
from app.api.routers import books as books_router  
from app.api.routers import loans as loans_router
from app.api.routers import orders as orders_router
from app.api.routers import statistics as statistics_router

app = FastAPI()
app.add_middleware(ResponseTimeMiddleware)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router.router) 
app.include_router(users_router.router)
app.include_router(books_router.router)
app.include_router(loans_router.router)
app.include_router(orders_router.router)
app.include_router(statistics_router.router)

@app.get("/")
def test() -> dict[str, str]:
    return {"status": "ok"}
