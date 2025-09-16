from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# User model (extends Better-Auth user)
class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: str
    role: str  # farmer, buyer, admin
    name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None  # For farmers/buyers
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Product model
class Product(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    farmer_id: PyObjectId
    name: str
    description: str
    category: str  # e.g., vegetables, fruits, grains
    price: float
    quantity: int
    unit: str  # e.g., kg, pieces
    images: List[str] = []  # URLs
    location: str
    harvest_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    is_available: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Order model
class OrderItem(BaseModel):
    product_id: PyObjectId
    quantity: int
    price: float

class Order(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    buyer_id: PyObjectId
    items: List[OrderItem]
    total_amount: float
    status: str = "pending"  # pending, confirmed, shipped, delivered, cancelled
    shipping_address: str
    payment_status: str = "pending"  # pending, paid, failed
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Learning Content model
class LearningContent(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: str
    content_type: str  # text, video, image
    content_url: Optional[str] = None
    text_content: Optional[str] = None
    category: str  # crop type, season
    tags: List[str] = []
    created_by: PyObjectId  # admin or expert
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Testimony model
class Testimony(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    title: str
    content: str
    rating: int  # 1-5
    images: List[str] = []
    is_featured: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Analytics model
class Analytics(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    type: str  # product_trends, demand_prediction, regional_data
    data: dict  # Flexible data structure
    date_range: dict  # start_date, end_date
    region: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}