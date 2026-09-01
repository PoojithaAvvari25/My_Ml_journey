from fastapi import FastAPI

app = FastAPI()
#creating route for the root endpoint
@app.get("/")
def hello():
    return {"message": "Hello, World!"}

@app.get("/greet{name}")
def greet(name: str):
    return {"message":f"Hii {name}"}


@app.get("/greet/{name}")
def greet(name: str):
    return {"message":f"Hii {name} Good evening"}
