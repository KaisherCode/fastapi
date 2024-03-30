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