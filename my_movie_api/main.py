from fastapi import FastAPI,Path,Query
from fastapi.responses import HTMLResponse,JSONResponse
from pydantic import BaseModel, Field,ConfigDict
from typing import Optional,List

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

class Movie(BaseModel):
    id: Optional[int] = None
    title:str = Field(min_length=5,max_length=15)
    overview:str = Field(min_length=15,max_length=50)
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

@app.get("/movies",tags=["movies"],response_model=List[Movie],status_code=200)
def get_movies()->List[Movie]:
    return JSONResponse(status_code=200,content=movies)

# @app.get("/movies/{id}",tags=["movies"])
# def get_movies_by_id(id:int):
#     for item in movies:
#         if item["id"]==id:
#             return item
#     return []

@app.get("/movie/{id}",tags=["movies"],response_model=Movie)
def get_movie_by_id(id:int = Path(ge=1,le=2000))->Movie:
    item = [i for i in movies if i["id"]==id] 
    if item == []:
        return JSONResponse(content=[],status_code=404)
    return JSONResponse(content=item)
        
# @app.get("/movies/",tags=["movies"])
# def get_movies_by_category(category:str,year:int):
#     return category

@app.get("/movies/",tags=["movies"],response_model=List[Movie])
def get_movies_by_cetegory(category:str=Query(min_length=5,max_lenth=15))->List[Movie]:
    data=[movie for movie in movies if movie["category"]==category]
    if data == []:
        return JSONResponse(content=[],status_code=404)
    return JSONResponse(content=data)
    
@app.post("/movies",tags=["movies"],response_model=dict,status_code=201)
def create_movies(movie:Movie)->dict:
    movies.append(movie)
    return JSONResponse(status_code=201,content={"message":"Se registró la película"})

@app.put("/movies/{id}",tags=["movies"],response_model=dict,status_code=200)
def update_movie(id:int,movie:Movie)->dict:
    for item in movies:
        if item["id"]==id:
            item["title"]==movie.title
            item["overview"]==movie.overview
            item["year"]==movie.year
            item["rating"]==movie.rating
            item["category"]==movie.category
            return JSONResponse(status_code=200,content={"message":"Se ha modificado la película"})
            
@app.delete("/movies/",tags=["movies"],response_model=dict,status_code=200)
def delete_movie(id:int)->dict:
    for item in movies:
        if item["id"]==id:
            movies.remove(item)
            return JSONResponse(status_code=200,content={"message":"Se ha eliminado la película"})
    # global movies
    # movies = [movie for movie in movies if movie["id"] != id]
    # return movies

