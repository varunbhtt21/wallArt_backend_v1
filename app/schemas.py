from pydantic import BaseModel, Field
from typing import List, Optional


class Url(BaseModel):
    image_url : str

    class Config:
        orm_mode = True


class Product(BaseModel):
    id : int = Field(alias="product_id")
    name : str
    price : int
    urls : List[Url]
    rating : int
    description : str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True        


class Category(BaseModel):
    id : int 
    name : str
    image : str
    products : List[Product]

    class Config:
        orm_mode = True


class FetchCategory(BaseModel):
    id : int
    name : str
    image : str

    class Config:
        orm_mode = True


class Cart(BaseModel):
    product_id : int 
    quantity : int
    user_id : int

    class Config:
        orm_mode = True

class CartRequest(BaseModel):
    product_id : int 
    quantity : int

    class Config:
        orm_mode = True


class CartResponse(BaseModel):
    product_id : int 
    product_name : str
    price : int
    quantity : int
    total_price : int

    class Config:
        orm_mode = True





# class OrdersResponse(BaseModel):
#     id : str
#     entity : str
#     amount : int
#     amount_paid : int
#     amount_due : int
#     currency : str
#     receipt : str
#     status : str
#     attempts : int
#     notes : List
#     # created_at : str

#     class Config:
#         orm_mode = True



class Payment(BaseModel):
    razorpay_payment_id : str
    razorpay_order_id : str
    razorpay_signature : str
    name : str
    email : str
    contactNo : str
    address : str
    pincode : str
    city : str
    area : str

    class Config:
        orm_mode = True
   