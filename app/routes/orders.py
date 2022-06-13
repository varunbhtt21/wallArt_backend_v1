import razorpay
from fastapi import APIRouter
import schemas, database, models
from database import get_db
from fastapi import FastAPI, Depends
from typing import Dict, List, Optional, Tuple
from schemas import Product, Category, Payment
from sqlalchemy.orm import Session
import json
import ast
import os
from os.path import join, dirname
from dotenv import load_dotenv


router = APIRouter(
    prefix="/orders",
    tags=['orders']
)



@router.post("", response_model=schemas.OrdersResponse)
def orderPlaced(request: schemas.OrdersRequest, db: Session = Depends(database.get_db)):

    os.getenv("CALENDY_CLIENT_ID")

    dotenv_path = join(dirname(__file__), ".env")
    load_dotenv(override=True)
    API_KEY = os.environ.get("API_KEY")
    API_SECRET = os.environ.get("API_SECRET")

    client = razorpay.Client(auth=(API_KEY, API_SECRET))

    data_string = json.dumps(request, default=lambda o: o.__dict__)
    data_dictionary = ast.literal_eval(data_string)
    
    payment = client.order.create(data=data_dictionary)
    print(payment)
   
    return payment


@router.post("/payment", response_model=str)
def orderPlaced(request: schemas.Payment, db: Session = Depends(database.get_db)):
    client = razorpay.Client(auth = ('rzp_live_C80HDnSFL9Wxmb', 'nIgSCMYd7srvIs3x0aS9OxYs'))

    data_string = json.dumps(request, default=lambda o: o.__dict__)
    data_dictionary = ast.literal_eval(data_string)

    print(data_dictionary)
    try:
        status = client.utility.verify_payment_signature(data_dictionary)
        return "success"
    except:
        return "failed"


