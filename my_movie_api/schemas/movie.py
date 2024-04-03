from pydantic import BaseModel, Field,ConfigDict
from typing import Optional

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