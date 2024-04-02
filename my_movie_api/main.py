from fastapi import FastAPI,Path,Query,Request,HTTPException,Depends
from fastapi.responses import HTMLResponse,JSONResponse
from pydantic import BaseModel, Field,ConfigDict
from typing import Optional,List
from jwt_manager import create_token,validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

movies=[
    {
        "id":1,
        "title":"Avatar",
        "overview":"En un axuberante planeta llamado Pandora viven los Na'vi seres que ...",
        "year":2009,
        "rating":7.8,
        "category":"Acción"
    },
    {
        "id":2,
        "title":"Reverdale",
        "overview":"Riverdale is an American television series based on the characters of Archie Comics.",
        "year":2017,
        "rating":8,
        "category":"Teen Drama Mystery"
    }
]

app = FastAPI()
app.title = "Mi app con FastAPI"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self,request:Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403,detail="Credenciales inválidos")          

class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id: Optional[int] = None
    title:str = Field(min_length=5,max_length=20)
    overview:str = Field(min_length=15,max_length=60)
    year:int = Field(le=2022)
    rating: float = Field(ge=1, le=10)
    category:str = Field(min_length=5,max_length=15)
    
    model_config = ConfigDict(
        json_schema_extra = {
        'examples': [
                {
                    "id": 1,
                    "title": "Mi pelicula",
                    "overview": "Descripcion de la pelicula",
                    "year":2022,
                    "rating": 9.8,
                    "category": "Acción"
                }
            ]
    })

@app.get("/",tags=["home"])
def message():
    return HTMLResponse('<h1>Hello World!</h1>')

@app.post("/login",tags=["auth"])
def login(user:User):
    if user.email == "admin@gmail.com" and user.password == "admin123":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200,content=token)

@app.get("/movies",tags=["movies"],response_model=List[Movie],status_code=200,dependencies=[Depends(JWTBearer())])
def get_movies()->List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@app.get("/movie/{id}",tags=["movies"],response_model=Movie)
def get_movie_by_id(id:int = Path(ge=1,le=2000))->Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id==id).first()
    if not result:
        return JSONResponse(status_code=404,content={"message":"No encontrado"})
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@app.get("/movies/",tags=["movies"],response_model=List[Movie])
def get_movies_by_cetegory(category:str=Query(min_length=5,max_lenth=15)) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category==category).all()
    if not result:
        return JSONResponse(status_code=404,content={"message":"They are no films with that category"})
    return JSONResponse(status_code=200,content=jsonable_encoder(result))
    
@app.post("/movies",tags=["movies"],response_model=dict,status_code=201)
def create_movies(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201,content={"message":"Se registró la película"})

@app.put("/movies/{id}",tags=["movies"],response_model=dict,status_code=200)
def update_movie(id:int,movie:Movie)->dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id==id).first()
    if not result:
        return JSONResponse(status_code=404,content={"message":"Category Not found"})
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category  
    db.commit() 
    return JSONResponse(status_code=200,content={"message":"Movie has been modified"})
            
@app.delete("/movies/",tags=["movies"],response_model=dict,status_code=200)
def delete_movie(id:int)->dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id==id).first()
    if not result:
        return JSONResponse(status_code = 404,content= {"message":"Category not found"})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200,content={"message":"Movie has been removed"})
    
