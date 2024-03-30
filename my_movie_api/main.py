from fastapi import FastAPI
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

@app.get("/movies/{id}",tags=["movies"])
def getmovies_by_id(id:int):
    item = [i for i in movies if i["id"]==id] 
    if item == []:
        return f"Not found movie"
    return item
        
        
        