from fastapi import FastAPI,Body
from fastapi.responses import HTMLResponse

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

@app.get("/movie/{id}",tags=["movie"])
def get_movie_by_id(id:int):
    item = [i for i in movies if i["id"]==id] 
    if item == []:
        return f"Not found movie"
    return item
        
# @app.get("/movies/",tags=["movies"])
# def get_movies_by_category(category:str,year:int):
#     return category

@app.get("/movies/",tags=["movies"])
def get_movies_by_cetegory(category:str):
    filtered_by_category=[movie for movie in movies if movie["category"]==category]
    if filtered_by_category == []:
        return f"Not found category"
    return filtered_by_category
    
@app.post("/movies",tags=["movies"])
def create_movies(
    id:int=Body(),
    title:str=Body(),
    overview:str=Body(),
    year:int=Body(),
    rating:float=Body(),
    category:str=Body()):
    movies.append({
        "id":id,
        "title":title,
        "overview":overview,
        "year":year,
        "rating":rating,
        "category":category
    })
    return movies

@app.put("/movies/{id}",tags=["movies"])
def update_movie(
    id:int,
    title:str=Body(),
    overview:str=Body(),
    year:int=Body(),
    rating:float=Body(),
    category:str=Body()):
    for item in movies:
        if item["id"]==id:
            item["title"]==title
            item["overview"]==overview
            item["year"]==year
            item["rating"]==rating
            item["category"]==category
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
