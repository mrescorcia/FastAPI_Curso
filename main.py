from fastapi import FastAPI

app = FastAPI()

#-- La siguiente es una path operation
@app.get("/")
def home():
    return {"Hello": "World"}

# -- uvicorn main:app --reload (para correr en terminal)