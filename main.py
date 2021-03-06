#                                           Python
#realizaremos tipado estatico con typing
from typing import Optional

#libreria Pydantic, clase BaseModel
from pydantic import BaseModel

#                                           FastAPI
from fastapi import FastAPI
from fastapi import Body
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