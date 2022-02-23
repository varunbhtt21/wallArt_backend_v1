from products.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, String, JSON, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func



class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)

    category_id = Column(Integer, ForeignKey('categories.id'))
    categories = relationship("Categories", back_populates="products")

    price = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    description = Column(String)
    urls = relationship("Url", back_populates='products')

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Url(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'))
    products = relationship("Products", back_populates="urls")


class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    products = relationship("Products", back_populates="categories")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

