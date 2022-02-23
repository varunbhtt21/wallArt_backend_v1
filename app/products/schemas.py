from pydantic import BaseModel
from typing import List, Optional


class Url(BaseModel):
    image_url : str

    class Config:
        orm_mode = True


class Product(BaseModel):
    id : int
    name : str
    price : int
    urls : List[Url]
    rating : int
    description : str

    class Config:
        orm_mode = True


class Category(BaseModel):
    id : int 
    name : str
    products : List[Product]

    class Config:
        orm_mode = True

