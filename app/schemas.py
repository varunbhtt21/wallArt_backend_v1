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

class CategoryFetch(BaseModel):
    id : int
    name : str
    image : str

    class Config:
        orm_mode = True


class Cart(BaseModel):
    product_id : int 
    quantity : int
    products : Product

    class Config:
        orm_mode = True

class CartRequest(BaseModel):
    product_id : int 
    quantity : int

    class Config:
        orm_mode = True


class CartResponse(BaseModel):
    product_id : int 
    product_name : Optional[str] = None
    price : Optional[int] = None
    quantity : Optional[int] = None
    total_price : Optional[int] = None

    class Config:
        orm_mode = True


class OrdersRequest(BaseModel):
    amount : int
    currency : str
    receipt : str
    user_id : int

    class Config:
        orm_mode = True


class OrdersResponse(BaseModel):
    id : str
    amount : int
    currency : str
    # created_at : str

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

    class Config:
        orm_mode = True
   