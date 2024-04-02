from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from jwt_manager import create_token
from config.database import engine, Base
from middlewares.error_handler import ErrorHanddler
from routers.movie import movie_router

app = FastAPI()
app.title = "Mi app con FastAPI"
app.version = "0.0.1"

app.add_middleware(ErrorHanddler)
app.include_router(movie_router)


Base.metadata.create_all(bind=engine)   


class User(BaseModel):
    email: str
    password: str       


@movie_router.post("/login",tags=["auth"])
def login(user:User):
    if user.email == "admin@gmail.com" and user.password == "admin123":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200,content=token)

    
