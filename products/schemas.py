from pydantic import BaseModel

class Product(BaseModel):
    name : str
    price : int
    image_url : str
    rating : int

