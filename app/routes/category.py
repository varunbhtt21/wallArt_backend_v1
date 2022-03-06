from fastapi import APIRouter
import schemas, database, models
from database import get_db
from fastapi import FastAPI, Depends
from typing import Dict, List, Optional, Tuple
from schemas import Product, Category
from sqlalchemy.orm import Session
from oauth2 import get_current_user
import routes

router = APIRouter(
    prefix="/category",
    tags=['category']
)

def addUrls(urls_list, db):
    url = models.Url(image_url=urls_list.image_url)
    db.add(url)
    db.commit()
    return url


def addProducts(current, db):
    product = models.Products(name=current.name, 
                                    price = current.price,
                                    description = current.description,
                                    rating = current.rating)
    for url in current.urls:
        product.urls.append(addUrls(url, db))
        
    db.add(product)
    db.commit()

    return product


@router.post("/",response_model=Category)
def createCategory(request: schemas.Category, db: Session = Depends(get_db)):
    new_category = models.Categories(name=request.name)
    for current in request.products:
        new_category.products.append(addProducts(current, db))
        
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get("/",response_model=List[Category])
def allCategories(db: Session = Depends(get_db),current_user: routes.user.User = Depends(get_current_user)):
    categories = db.query(models.Categories).all()
    return categories