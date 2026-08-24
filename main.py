from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Hello API")


class Item(BaseModel):
    name: str
    price: float


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.post("/items")
def create_item(item: Item):
    return {"created": item}
