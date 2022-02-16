from fastapi import FastAPI, Depends
from products import schemas, models
from products.database import engine, SessionLocal
from sqlalchemy.orm import Session

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
                                    price = request.price, image_url = request.image_url,
                                    rating = request.rating)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.get("/products")
def allProducts(db: Session = Depends(get_db)):
    products = db.query(models.Products).all()
    return products

@app.get("/product/{id}")
def show(id, db: Session = Depends(get_db)):
    product = db.query(models.Products).filter(models.Products.id == id).first()
    return product


@app.get("/")
def allProducts(db: Session = Depends(get_db)):
    return "Hello"