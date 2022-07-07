# from msilib.schema import Class
from unicodedata import name
import razorpay
from fastapi import APIRouter
from models import Orders, OrderStatus, OrderDetails
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


router = APIRouter(
    prefix="/orders",
    tags=['orders']
)



class OrdersRequest(BaseModel):
    amount : int
    currency : str
    receipt : str
    # name : str
    # email : str
    # contactNo : str
    # address : str
    # pincode : str
    # city : str
    # area : str
    

    class Config:
        orm_mode = True


class OrdersResponse(BaseModel):
    amount : int
    currency : str
    receipt : str
    

    class Config:
        orm_mode = True



@router.post("", response_model=OrdersResponse)
def orderPlaced(request: OrdersRequest, db: Session = Depends(database.get_db)):

    
    client = razorpay.Client(auth=(os.environ.get("API_KEY"), os.environ.get("API_SECRET")))

    data = { 
                "amount": request.amount, 
                "currency": request.currency, 
                "receipt": request.receipt }

    payment = client.order.create(data=data)
    
#     key_id,key_secret
# rzp_test_g7Iw6XOgt0GIUE,IV4Twq5uOGTYDr36oogjTcrj

    # if payment["status"]=="created":
    #     status = OrderStatus.CREATED

    # order = Orders(
    #                id = payment["id"],
    #                amount = payment["amount"],
    #                amount_paid = payment["amount_paid"],
    #                amount_due = payment["amount_due"],
    #                currency = payment["currency"],
    #                receipt = payment["receipt"],
    #                status = status,
    #                attempts = payment["attempts"]
    #                )
    
    # order_detail = OrderDetails(
    #                     name = request.name,
    #                     email = request.email,
    #                     contact = request.contactNo,
    #                     address = request.address,
    #                     pincode = request.pincode,
    #                     city = request.city,
    #                     area = request.area
    #                  )

   
    # order_detail.orders.append(order)
   
    # db.add(order_detail)
    # db.add(order)
    # db.commit()
    # db.refresh(order)

    return payment



@router.post("/payment", response_model=str)
def orderPlaced(request: schemas.Payment, db: Session = Depends(database.get_db)):
    
    client = razorpay.Client(auth=(os.environ.get("API_KEY"), os.environ.get("API_SECRET")))
    data = {
            "razorpay_payment_id": request.razorpay_payment_id,
            "razorpay_order_id": request.razorpay_order_id,
            "razorpay_signature": request.razorpay_signature
    }

    order = (
            db.query(Orders)
            .filter(Orders.id == request.razorpay_order_id)
            .first()
        )
    
    
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

