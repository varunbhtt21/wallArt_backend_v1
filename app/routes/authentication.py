from http.client import HTTPException
from fastapi import APIRouter, HTTPException, Response, status
from pydantic import BaseModel
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


router = APIRouter(
    prefix="/token",
    tags=['Authentication']
)

class Login(BaseModel):
    username : str
    password : str

    class Config:
        orm_mode = True



@router.post("")
def login(request : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    if not Hash.verifyPassword(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect Password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
