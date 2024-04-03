from fastapi import FastAPI
from config.database import engine, Base
from middlewares.error_handler import ErrorHanddler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
app.title = "Mi app con FastAPI"
app.version = "0.0.1"

app.add_middleware(ErrorHanddler)
app.include_router(movie_router)
app.include_router(user_router)


Base.metadata.create_all(bind=engine)   

