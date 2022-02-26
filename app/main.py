from fastapi import FastAPI, Depends
from products import schemas, models
from products.database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Dict, List, Optional, Tuple
from products.schemas import Url, Product, Category, Cart, CartResponse, CartRequest
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/product", response_model=Product)
def createProduct(request: schemas.Product, db: Session = Depends(get_db)):
    
    new_product = models.Products(name=request.name, 
                                    price = request.price,
                                    description = request.description,
                                    rating = request.rating)
    
    for i in request.urls:
        url = models.Url(image_url=i.image_url)
        
        print(new_product.urls)

        new_product.urls.append(url)
        print(new_product.urls)
        db.add(url)
        db.commit()

    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product



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


@app.post("/category",response_model=Category)
def createCategory(request: schemas.Category, db: Session = Depends(get_db)):
    new_category = models.Categories(name=request.name)
    for current in request.products:
        new_category.products.append(addProducts(current, db))
        
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


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

@app.post("/cart/{user_id}",response_model=List[CartResponse])
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


@app.get("/cart",response_model=List[CartResponse])
def allCartItems(db: Session = Depends(get_db)):
    cartItems = db.query(models.CartItems).all()
    return cartItems

@app.get("/products",response_model=List[Product])
def allProducts(db: Session = Depends(get_db)):
    products = db.query(models.Products).all()
    return products


@app.get("/categories",response_model=List[Category])
def allCategories(db: Session = Depends(get_db)):
    categories = db.query(models.Categories).all()
    return categories

@app.get("/urls")
def allUrls(db: Session = Depends(get_db)):
    urls = db.query(models.Url).all()
    return urls

@app.get("/product/{id}",response_model=Product)
def show(id, db: Session = Depends(get_db)):
    product = db.query(models.Products).filter(models.Products.id == id).first()
    return product


@app.get("/")
def test(db: Session = Depends(get_db)):
    return "Hello"