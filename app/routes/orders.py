from locale import currency
import razorpay
from fastapi import APIRouter
from schemas import Cart
import schemas, database, models
from database import get_db
from fastapi import FastAPI, Depends
from typing import Dict, List, Optional, Tuple
from schemas import Product, Category, Payment
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import json
import ast
from routes.user import ShowUser


router = APIRouter(
    prefix="/orders",
    tags=['orders']
)

class ProductCart(BaseModel):
    name : str
    price : int
    rating : int
    description : str
    class Config:
        orm_mode = True


class CartOrder(BaseModel):
    quantity : int
    products : ProductCart
    class Config:
        orm_mode = True

class Order(BaseModel):
    id : str
    amount : int 
    currency : str
    receipt : str
    status : str
    users : ShowUser
    cart : Cart

    class Config:
        orm_mode = True


@router.post("", response_model=schemas.OrdersResponse)
def createOrder(request: schemas.OrdersRequest, db: Session = Depends(database.get_db)):

    client = razorpay.Client(auth=("rzp_test_xvp0YKDLxMR9mG", "zFrRXxSSzxbFYqSrUIwFfYph"))

    data_string = json.dumps(request, default=lambda o: o.__dict__)
    data_dictionary = ast.literal_eval(data_string)
    del data_dictionary["user_id"]
    payment = client.order.create(data=data_dictionary)

    if payment:
        order = models.Order(id = payment['id'], 
                            amount = payment['amount'], currency = payment['currency'],
                            receipt = payment['receipt'], status = payment['status'])
        user = db.query(models.User).filter(models.User.id == request.user_id).first()
        user.orders.append(order)
        db.add(order)
        db.commit()
        db.refresh(order)
   
    return payment


@router.post("/payment", response_model=str)
def verifyPayment(request: schemas.Payment, db: Session = Depends(database.get_db)):
    client = razorpay.Client(auth = ('rzp_test_xvp0YKDLxMR9mG', 'zFrRXxSSzxbFYqSrUIwFfYph'))

    data_string = json.dumps(request, default=lambda o: o.__dict__)
    data_dictionary = ast.literal_eval(data_string)

    try:
        status = client.utility.verify_payment_signature(data_dictionary)
        return "success"
    except:
        return "failed"


@router.get("", response_model=List[Order])
def allOrder(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    return orders