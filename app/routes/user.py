import email
from http.client import HTTPException
from urllib import request
from fastapi import APIRouter, HTTPException, Response, status
from pydantic import BaseModel
import schemas, database, models
from database import get_db
from fastapi import FastAPI, Depends
from typing import Dict, List, Optional, Tuple
from schemas import Product
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import utils
from utils.hashing import Hash


router = APIRouter(
    prefix="/user",
    tags=['users']
)


class User(BaseModel):
    name : str
    email : str
    password : str

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    name : str
    email : str

    class Config:
        orm_mode = True
   

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated = "auto")


@router.post("", response_model=ShowUser)
def createUser(request : User, db: Session = Depends(get_db)):
    hashed_password = pwd_cxt.hash(request.password)
    new_user = models.User(name = request.name, email = request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=ShowUser)
def get_user(id : int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return user



