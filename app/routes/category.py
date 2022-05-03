from email.mime import image
from fastapi import APIRouter
from models import Categories
import schemas, database, models
from database import get_db
from fastapi import FastAPI, Depends
from typing import Dict, List, Optional, Tuple
from schemas import Product, Category, FetchCategory
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
    new_category = models.Categories(name=request.name, image = request.image)
    print(vars(new_category))
    for current in request.products:
        new_category.products.append(addProducts(current, db))
    
    print(new_category)

    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get("/",response_model=List[Category])
def allCategories(db: Session = Depends(get_db)):
    categories = db.query(models.Categories).all()
    return categories


@router.get("/fetch",response_model=List[FetchCategory])
def fetchCategory(db: Session = Depends(get_db)):
    categories = db.query(models.Categories).all()
    return categories


@router.get("/fetch/{id}",response_model=Category)
def fetchCategoryById(id, db: Session = Depends(get_db)):
    return db.query(models.Categories).filter(models.Categories.id == id).first()
