from fastapi import APIRouter
import schemas, database, models
from database import get_db
from fastapi import FastAPI, Depends
from typing import Dict, List, Optional, Tuple
from schemas import CartResponse, CartRequest, Cart
from sqlalchemy.orm import Session
from oauth2 import get_current_user
import routes

router = APIRouter(
    prefix="/cart",
    tags=['cart']
)


# ,current_user: routes.user.User = Depends(get_current_user)
@router.post("/{user_id}",response_model=List[CartResponse])
def checkout(request: List[CartRequest] ,user_id: int, db: Session = Depends(get_db)):
    
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



@router.get("/",response_model=List[Cart])
def allCartItems(db: Session = Depends(get_db)):
    cartItems = db.query(models.CartItems).all()
    return cartItems