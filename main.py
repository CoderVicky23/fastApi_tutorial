from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

# from . import schemas

app = FastAPI()

@app.get("/")
def index():
    return {"data":
            {"name": "Vicky", "age": 23}
    }

@app.get("/blog")
def blog(limit: int = 100, published: bool = 0, sort: Optional[str] = None):
    if published:
        return {'data': f'{limit} published blogs from db by {sort}'}
    else:
        return {'data': f'{limit} blogs from db'}


@app.get("/user/{id}/comments")
def comments(id: int):
    return {
        "user": id,
        "comments": {1, 2, 3}
    }

class Blog(BaseModel):
    title: str
    content: str
    published: Optional[bool]

@app.post("/blog")
def createBlog(request: Blog):
    return {
        "data": f"Blog created using {request.title}"
    }




# @app.post("/blog")
# def create(request: schemas.Blog):
#     return {
#         "title": request.title,
#         "body": request.body,
#     }