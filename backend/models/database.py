from sqlalchemy import create_engine, Column, String, Float, Integer, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./retail.db")

# SQLite-specific configuration
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Product(Base):
    __tablename__ = "products"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    rating = Column(Float)
    image_url = Column(String)
    description = Column(String)
    category = Column(String, index=True)
    brand = Column(String, index=True)
    sizes = Column(JSON)
    colors = Column(JSON)
    is_trending = Column(Boolean, default=False)
    is_seasonal = Column(Boolean, default=False)
    is_bestseller = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Inventory(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, index=True)
    warehouse_stock = Column(Integer)
    store_stocks = Column(JSON)  # {"Mumbai": 15, "Delhi": 20}
    last_updated = Column(DateTime, default=datetime.utcnow)


class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    loyalty_tier = Column(String, default="Silver")
    loyalty_points = Column(Integer, default=0)
    preferences = Column(JSON)
    browsing_history = Column(JSON)
    purchase_history = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, index=True)
    items = Column(JSON)
    subtotal = Column(Float)
    discount_amount = Column(Float)
    final_amount = Column(Float)
    payment_method = Column(String)
    payment_status = Column(String)
    transaction_id = Column(String)
    fulfillment_option = Column(String)
    fulfillment_status = Column(String)
    delivery_address = Column(String, nullable=True)
    store_location = Column(String, nullable=True)
    estimated_delivery = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
