from email import message
from http.client import HTTPException
from fastapi import APIRouter, HTTPException, Response, status
from pydantic import BaseModel
from models import CartItems
import models, token
from database import get_db
from fastapi import FastAPI, Depends
from typing import Dict, List, Optional, Tuple
from schemas import Product
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import utils
from utils.hashing import Hash
from routes.token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/token",
    tags=['Authentication']
)

class Login(BaseModel):
    username : str
    password : str

    class Config:
        orm_mode = True


# def login(request : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

@router.post("")
# def login(request : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
def login(request : Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    if not Hash.verifyPassword(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect Password")

    access_token = create_access_token(data={"sub": user.email})

    user = db.query(models.User).filter(models.User.email == user.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return {"access_token": access_token, "token_type": "bearer", "user_id":user.id}




class CartStore(BaseModel):
    product_id : int
    quantity : int

    class Config:
        orm_mode = True

@router.post("/logout/{user_id}")
def logout(user_id : int, request : List[CartStore], db: Session = Depends(get_db)):
    product_missing = False
    if not user_id:
        return JSONResponse({"message": "Please provide the user id"}, status_code=400)


    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user id")

    for val in request:
        cart = db.query(models.CartItems).filter(models.CartItems.product_id == val.product_id,
                                                 models.CartItems.user_id == user_id).first()
        if cart:
            cart.quantity = val.quantity
        else:
            cart = CartItems(product_id=val.product_id, quantity = val.quantity, user_id = user_id)
        
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    if product_missing:
        return JSONResponse({"message": "Some Products does not exist"}, status_code=200)
    else:
        return JSONResponse({"message": "Success"}, status_code=200)





