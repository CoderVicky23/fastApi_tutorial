from pydantic import BaseModel

class Item(BaseModel):
    title: str
    body: str
    published: bool = True

