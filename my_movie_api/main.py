from fastapi import FastAPI,Path,Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field,ConfigDict
from typing import Optional

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

@app.get("/movies",tags=["movies"])
def get_movies():
    return movies

# @app.get("/movies/{id}",tags=["movies"])
# def get_movies_by_id(id:int):
#     for item in movies:
#         if item["id"]==id:
#             return item
#     return []

@app.get("/movie/{id}",tags=["movies"])
def get_movie_by_id(id:int = Path(ge=1,le=2000)):
    item = [i for i in movies if i["id"]==id] 
    if item == []:
        return f"Not found movie"
    return item
        
# @app.get("/movies/",tags=["movies"])
# def get_movies_by_category(category:str,year:int):
#     return category

@app.get("/movies/",tags=["movies"])
def get_movies_by_cetegory(category:str=Query(min_length=5,max_lenth=15)):
    filtered_by_category=[movie for movie in movies if movie["category"]==category]
    if filtered_by_category == []:
        return f"Not found category"
    return filtered_by_category
    
@app.post("/movies",tags=["movies"])
def create_movies(movie:Movie):
    movies.append(movie)
    return movies

@app.put("/movies/{id}",tags=["movies"])
def update_movie(id:int,movie:Movie):
    for item in movies:
        if item["id"]==id:
            item["title"]==movie.title
            item["overview"]==movie.overview
            item["year"]==movie.year
            item["rating"]==movie.rating
            item["category"]==movie.category
            return movies
            
@app.delete("/movies/",tags=["movies"])
def delete_movie(id:int):
    for item in movies:
        if item["id"]==id:
            movies.remove(item)
            return movies
    # global movies
    # movies = [movie for movie in movies if movie["id"] != id]
    # return movies

