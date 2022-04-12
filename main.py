#                                           Python
#realizaremos tipado estatico con typing
import email
from importlib.resources import path
from operator import gt
from typing import Optional

#Clase para crear enumeraciones de String
from enum import Enum
from email_validator import validate_email

#libreria Pydantic, clase BaseModel
from pydantic import BaseModel, EmailStr, HttpUrl
from pydantic import Field

#                                           FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path
app = FastAPI()

#                                           Models
    

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"


class Location(BaseModel):
    city: str = Field(
        min_length=3,
        max_length=50
    )
    state: str = Field(
        min_length=3,
        max_length=50
    )
    country: str = Field(
        min_length=3,
        max_length=50
    )

    #---                automatic_body_examples
    class Config:
        schema_extra = {
            "example":{
                "city": "Malambo",
                "state": "Atlántico",
                "country": "Colombia"
            }
        }



class Person(BaseModel):
    firstName: str = Field(
        ...,
        min_length=0,
        max_length=50
    )
    lastName: str = Field(
        ...,
        min_length=0,
        max_length=50
    )
    age: int = Field(
        ...,
        gt=0,
        le=115
    )
    hairColor: Optional[HairColor] = Field(default=None)
    isMarried: Optional[bool] = Field(default=None)
    email: EmailStr = Field(
        ...
    )
    blogUrl: HttpUrl = Field(
        ...
    )

    #---                    automatic_body_examples
    class Config:
        schema_extra = {
            "example": {
                "first_name": "David",
                "last_name": "Escorcia Gomez",
                "age": 24,
                "hairColor": "white",
                "isMarried": False,
                "email": "escorciagomezdavid@gmail.com",
                "blogUrl": "http://www.google.com"
            }
        }


#-- La siguiente es una path operation
@app.get("/")
def home():
    return {"Hello": "World"}

# -- uvicorn main:app --reload (para correr en terminal)

# request and response
@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

#Validaciones: Query Parameters
@app.get("/person/detail")
def showPerson(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the Person Name. It's between 1 and 50 characters"
        ),
    age : str = Query(
        ...,
        title="Person Age",
        description="This is the Person Age. It's required"
        )
):
    return {name: age}

#validaciones: Path Parameters
@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        title="Person Id",
        description="This is the Person Id. It's required"
        )
):
    return {person_id: "It exist!"}

#-- Validaciones: Request Body
@app.put("/person/detail/{person_id}")
def updatePerson(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    #--combinamos los dos diccionarios para tener uno solo
    results = person.dict()
    results.update(location.dict())
    return results
    #return person