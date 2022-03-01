from fastapi import FastAPI, Depends
from products.database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Dict, List, Optional, Tuple
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routes import products, category, cart
import models
import database


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

app.include_router(products.router)
app.include_router(category.router)
app.include_router(cart.router)




@app.get("/")
def test(db: Session = Depends(database.get_db)):
    return "Hello"