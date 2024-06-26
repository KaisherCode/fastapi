from fastapi import Path,Query,Depends
from fastapi.responses import HTMLResponse,JSONResponse
from typing import List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie



from fastapi import APIRouter

movie_router = APIRouter()

@movie_router.get("/",tags=["home"])
def message():
    return HTMLResponse('<h1>Hello World!</h1>')

@movie_router.get("/movies",tags=["movies"],response_model=List[Movie],status_code=200,dependencies=[Depends(JWTBearer())])
def get_movies()->List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@movie_router.get("/movie/{id}",tags=["movies"],response_model=Movie)
def get_movie_by_id(id:int = Path(ge=1,le=2000))->Movie:
    db = Session()
    result = MovieService(db).get_movie_by_id(id)
    if not result:
        return JSONResponse(status_code=404,content={"message":" category id Not found"})
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@movie_router.get("/movies/",tags=["movies"],response_model=List[Movie])
def get_movies_by_cetegory(category:str=Query(min_length=5,max_lenth=15)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movie_by_category(category)
    if not result:
        return JSONResponse(status_code=404,content={"message":"They are no films with that category"})
    return JSONResponse(status_code=200,content=jsonable_encoder(result))
    
@movie_router.post("/movies",tags=["movies"],response_model=dict,status_code=201)
def create_movies(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201,content={"message":"The film was registered"})

@movie_router.put("/movies/{id}",tags=["movies"],response_model=dict,status_code=200)
def update_movie(id:int,movie:Movie)->dict:
    db = Session()
    result = MovieService(db).get_movie_by_id(id)
    if not result:
        return JSONResponse(status_code=404,content={"message":"Category id Not found"})
    MovieService(db).update_movie(id,movie)
    return JSONResponse(status_code=200,content={"message":"Movie has been modified"})
            
@movie_router.delete("/movies/",tags=["movies"],response_model=dict,status_code=200)
def delete_movie(id:int)->dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id==id).first()
    if not result:
        return JSONResponse(status_code = 404,content= {"message":"Category id not found"})
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200,content={"message":"Movie has been removed"})