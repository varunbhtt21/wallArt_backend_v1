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


router = APIRouter(
    prefix="/orders",
    tags=['orders']
)



@router.post("", response_model=schemas.OrdersResponse)
def orderPlaced(request: schemas.OrdersRequest, db: Session = Depends(database.get_db)):

    client = razorpay.Client(auth=("rzp_test_xvp0YKDLxMR9mG", "zFrRXxSSzxbFYqSrUIwFfYph"))

    data_string = json.dumps(request, default=lambda o: o.__dict__)
    data_dictionary = ast.literal_eval(data_string)
    
    payment = client.order.create(data=data_dictionary)
   
    return payment


