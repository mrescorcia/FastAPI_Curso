#                                           Python
#realizaremos tipado estatico con typing
from typing import Optional

#libreria Pydantic, clase BaseModel
from pydantic import BaseModel

#                                           FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path
app = FastAPI()

#                                           Models
class Person(BaseModel):
    firstName: str
    lastName: str
    age: int
    hairColor: Optional[str] = None
    isMarried: Optional[bool] = None


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