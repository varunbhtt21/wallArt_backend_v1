from fastapi import APIRouter
import schemas, database, models
from database import get_db
from fastapi import FastAPI, Depends
from typing import Dict, List, Optional, Tuple
from schemas import Product
from sqlalchemy.orm import Session
import routes.user, oauth2
from oauth2 import get_current_user

router = APIRouter(
    prefix="/product",
    tags=['products']
)

@router.post("", response_model=Product)
def createProduct(request: schemas.Product, db: Session = Depends(database.get_db),current_user: routes.user.User = Depends(get_current_user)):
    
    new_product = models.Products(name=request.name, 
                                    price = request.price,
                                    description = request.description,
                                    rating = request.rating)
    
    for i in request.urls:
        url = models.Url(image_url=i.image_url)

        new_product.urls.append(url)
        db.add(url)
        db.commit()

    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product



@router.post("/{id}/url")
def addUrl(request: schemas.Url, db: Session = Depends(get_db), current_user: routes.user.User = Depends(get_current_user)):
    
    url = models.Url(image_url = request.image_url, product_id = request.product_id)
    product = db.query(models.Products).filter(models.Products.id == id).first()
    
    product.urls.append(url)
    db.add(url)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/",response_model=List[Product])
def allProducts(db: Session = Depends(get_db),current_user: routes.user.User = Depends(get_current_user)):
    products = db.query(models.Products).all()
    return products


@router.get("/{id}",response_model=Product)
def show(id, db: Session = Depends(get_db)):
    product = db.query(models.Products).filter(models.Products.id == id).first()
    return product


@router.get("/urls")
def allUrls(db: Session = Depends(get_db)):
    urls = db.query(models.Url).all()
    return urls