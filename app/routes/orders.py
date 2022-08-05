# from msilib.schema import Class
from unicodedata import name
import razorpay
from fastapi import APIRouter
from models import CartItems
from models import Products
from models import Orders, OrderStatus, OrderDetails, OrdersProductInfo
import schemas, database, models
from database import get_db
from fastapi import FastAPI, Depends
from typing import Dict, List, Optional, Tuple
from schemas import Product, Category, Payment
from sqlalchemy.orm import Session
import json
import ast
from pydantic import BaseModel
import os
from os.path import join, dirname
from dotenv import load_dotenv
from utils.constants import API_KEY, API_SECRET
from pydantic import BaseModel, Field



router = APIRouter(
    prefix="/orders",
    tags=['orders']
)




class OrdersRequest(BaseModel):
    amount : int
    currency : str
    receipt : str

    class Config:
        orm_mode = True


class OrdersResponse(BaseModel):
    id : str = Field(alias="order_id")
    amount : int
    currency : str
    receipt : str

    class Config:
        orm_mode = True


class UserOrders(BaseModel):
    total_amount : int
    status : OrderStatus
    products : List[schemas.Product]

    class Config:
        orm_mode = True




@router.post("/payment", response_model=str)
def orderPlaced(request: Payment, db: Session = Depends(database.get_db)):
    
    client = razorpay.Client(auth=(os.environ.get("API_KEY"), os.environ.get("API_SECRET")))
    data = {
            "razorpay_payment_id": request.razorpay_payment_id,
            "razorpay_order_id": request.razorpay_order_id,
            "razorpay_signature": request.razorpay_signature,
    }

    order = (
            db.query(Orders)
            .filter(Orders.id == request.razorpay_order_id)
            .first()
        )
    
    # Adding Order Detail
    order_detail = OrderDetails(
                        name = request.name,
                        email = request.email,
                        contact = request.contactNo,
                        address = request.address,
                        pincode = request.pincode,
                        city = request.city,
                        area = request.area
                     )
    order_detail.orders.append(order)
    db.add(order_detail)
    
    
    order.razorpay_payment_id = request.razorpay_payment_id
    order.razorpay_signature = request.razorpay_signature

    try:
        status = client.utility.verify_payment_signature(data)
        order.status = OrderStatus.SUCCESS

        db.add(order)
        db.commit()
        db.refresh(order)

        return "success"
    except:
        order.status = OrderStatus.FAILED

        db.add(order)
        db.commit()
        db.refresh(order)

        return "failed"





@router.get("/{user_id}",response_model=List[UserOrders])
def allOrdersByUser(user_id : int ,db: Session = Depends(get_db)):
    orders = db.query(Orders).filter(Orders.user_id == user_id).all()

    all_orders = []

    for order in orders:
        order_product_info = db.query(OrdersProductInfo).filter(OrdersProductInfo.order_id == order.id).all()
        
        product_list = []
        for order_product in order_product_info:
            product_list.append(order_product.products)


        user_order = UserOrders(status=order.status, 
                                total_amount=order.amount,
                                products=product_list)
        all_orders.append(user_order)

    return all_orders



@router.post("/{user_id}", response_model=OrdersResponse)
def orderPlaced(user_id : int, request: OrdersRequest, db: Session = Depends(database.get_db)):

    client = razorpay.Client(auth=(os.environ.get("API_KEY"), os.environ.get("API_SECRET")))

    data = { 
                "amount": request.amount*100, 
                "currency": request.currency, 
                "receipt": request.receipt 
            }
    
    payment = client.order.create(data=data)
    

# key_id, key_secret
# rzp_test_g7Iw6XOgt0GIUE, IV4Twq5uOGTYDr36oogjTcrj

    if payment["status"]=="created":
        status = OrderStatus.CREATED

    order = Orders(
                   id = payment["id"],
                   amount = payment["amount"],
                   amount_paid = payment["amount_paid"],
                   amount_due = payment["amount_due"],
                   currency = payment["currency"],
                   receipt = payment["receipt"],
                   status = status,
                   attempts = payment["attempts"],
                   user_id = user_id
                   )
    
    db.add(order)
    db.commit()
    db.refresh(order)

    CartItems = db.query(models.CartItems).filter(models.User.id == user_id).all()
    for item in CartItems:
        order_product_info = OrdersProductInfo(order_id=payment["id"] ,
                                               product_id=item.product_id ,
                                               quantity=item.quantity)
        db.add(order_product_info)
        db.commit()
        db.refresh(order_product_info)
   

    return {
        "order_id" : payment["id"],
        "amount" : payment["amount"],
        "currency" : payment["currency"],
        "receipt" : payment["receipt"]
    }




