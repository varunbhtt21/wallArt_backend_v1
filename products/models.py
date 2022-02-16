from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, String, JSON, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func



class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    # categories = relationship("Categories", back_populates="products")
    price = Column(Integer, nullable=False)
    image_url = Column(String(500))
    rating = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



# class Categories(Base):
#     __tablename__ = 'categories'

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(50), nullable=False)
#     products = relationship("Products", back_populates="categories")
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())

