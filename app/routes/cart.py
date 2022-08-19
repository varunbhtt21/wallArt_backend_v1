from cgi import print_exception
from math import prod
from fastapi import APIRouter, HTTPException, status
from models import Url
import schemas, database, models
from database import get_db
from fastapi import FastAPI, Depends
from typing import Dict, List, Optional, Tuple
from schemas import CartResponse, CartRequest
from sqlalchemy.orm import Session
from oauth2 import get_current_user
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import routes

router = APIRouter(
    prefix="/cart",
    tags=['cart']
)



@router.post("/{user_id}",response_model=List[CartResponse])
def checkout(request: List[CartRequest] ,user_id: int, db: Session = Depends(get_db),current_user: routes.user.User = Depends(get_current_user)):
    
    output = []
    for item in request:
        product = db.query(models.Products).filter(models.Products.id == item.product_id).first()
        
        cart = models.CartItems(quantity=item.quantity, user_id=user_id)
        product.cartitems.append(cart)

        db.add(product)
        db.add(cart)
        db.commit()
        db.refresh(product)

        cartResponse = CartResponse(product_id = product.id, product_name = product.name,
                         price = product.price, quantity = item.quantity, total_price = product.price*item.quantity)
        output.append(cartResponse)
    
    return output


class CartItem(BaseModel):
    product_id : int 
    name : str
    url : str
    price : int
    quantity : int

    class Config:
        orm_mode = True


@router.get("/{user_id}",response_model=List[CartItem])
def allCartItems(user_id: int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user id")

    cartItems = db.query(models.CartItems).all()
    allItems = []
    for item in cartItems:
        product = db.query(models.Products).filter(models.Products.id == item.product_id, models.User.id == user_id).first()
        if product is None:
            continue
        new_cart_item = CartItem(product_id = item.product_id,
                                name = product.name,
                                url = product.urls[0].image_url,
                                price = product.price,
                                quantity = item.quantity)
        allItems.append(new_cart_item)

    return allItems

@router.get("/clear/{user_id}")
def clearCart(user_id:int, db: Session = Depends(get_db)):
    try:
        db.query(models.CartItems).filter(models.CartItems.user_id == user_id).delete()
        db.commit()

    except Exception as e:
        print(e)
        return JSONResponse(status_code=502, 
                            content={"message": "Failed"})
    
    return JSONResponse(status_code=200, 
                        content={"message": "Success"})

    
