from fastapi import FastAPI, Depends
from products import schemas, models
from products.database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Dict, List, Optional, Tuple
from products.schemas import Url, Product
from fastapi.responses import JSONResponse


from pprint import pprint

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/product")
def createProduct(request: schemas.Product, db: Session = Depends(get_db)):
    
    
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

@app.post("/product/{id}/url")
def addUrl(request: schemas.Url, db: Session = Depends(get_db)):
    
    url = models.Url(image_url = request.image_url, product_id = request.product_id)
    product = db.query(models.Products).filter(models.Products.id == id).first()
    
    product.urls.append(url)
    db.add(url)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@app.get("/products",response_model=List[Product])
def allProducts(db: Session = Depends(get_db)):
    products = db.query(models.Products).all()
    return products

@app.get("/urls")
def allUrls(db: Session = Depends(get_db)):
    urls = db.query(models.Url).all()
    return urls

@app.get("/product/{id}")
def show(id, db: Session = Depends(get_db)):
    product = db.query(models.Products).filter(models.Products.id == id).first()
    return product


@app.get("/")
def test(db: Session = Depends(get_db)):
    return "Hello"