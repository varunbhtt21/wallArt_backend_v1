from products.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, String, JSON, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func
import enum




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

    cartitems = relationship("CartItems", back_populates='products')

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
    image = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



class CartItems(Base):
    __tablename__ = "cartitems"
    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(Integer, ForeignKey('products.id'))
    products = relationship("Products", back_populates='cartitems')

    quantity = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    orders = relationship("Orders", back_populates="users")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class OrderStatus(enum.Enum):
    CREATED = "CREATED"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class OrderDetails(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    contact = Column(String(255), nullable=False)
    address = Column(String(512), nullable=False)
    pincode = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    area = Column(String(255), nullable=False)

    orders = relationship("Orders", back_populates="order_details")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class OrdersProductInfo(Base):
    __tablename__ = "orders_product_info"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String(255))
    product_id = Column(Integer, ForeignKey('products.id'))
    products = relationship("Products")
    quantity = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



class Orders(Base):
    __tablename__ = "orders"
    id = Column(String(255), primary_key=True, index=True)
    amount = Column(Integer, nullable=False)
    amount_paid = Column(Integer, nullable=False)
    amount_due = Column(Integer, nullable=False)
    currency = Column(String(255), nullable=False)
    receipt = Column(String(255), nullable=False)
    status = Column(Enum(OrderStatus))
    attempts = Column(Integer, nullable=False)
    razorpay_payment_id = Column(String(255))
    razorpay_signature = Column(String(512))

    order_details_id = Column(Integer, ForeignKey(OrderDetails.id))
    order_details = relationship("OrderDetails", back_populates="orders")

    user_id = Column(Integer, ForeignKey(User.id))
    users = relationship("User", back_populates="orders")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


