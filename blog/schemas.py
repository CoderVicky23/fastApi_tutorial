from pydantic import BaseModel
from typing import List, Optional

class Blog(BaseModel):
    title: str
    body: str


class User(BaseModel):
    name: str
    email: str
    password: str

class SingleUser(BaseModel):
    name: str
    email: str

class ShowUser(BaseModel):
    id: int
    name: str
    email: str
    blogs: List[Blog]

    class config:
        orm_mode = True

class ShowBlog(BaseModel):
    title: str
    body: str
    creator: SingleUser
    
    class config:
        orm_mode = True