from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import List
from ..models import Product, PyObjectId
from ..database import get_database

router = APIRouter()

@router.post("/products/", response_model=Product)
async def create_product(product: Product, db: AsyncIOMotorDatabase = Depends(get_database)):
    product_dict = product.dict(by_alias=True)
    result = await db.products.insert_one(product_dict)
    product.id = result.inserted_id
    return product

@router.get("/products/", response_model=List[Product])
async def read_products(skip: int = 0, limit: int = 10, db: AsyncIOMotorDatabase = Depends(get_database)):
    products = await db.products.find().skip(skip).limit(limit).to_list(length=limit)
    return [Product(**product) for product in products]

@router.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    product = await db.products.find_one({"_id": ObjectId(product_id)})
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**product)

@router.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: str, product_update: Product, db: AsyncIOMotorDatabase = Depends(get_database)):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    update_data = product_update.dict(exclude_unset=True, by_alias=True)
    result = await db.products.update_one({"_id": ObjectId(product_id)}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    updated_product = await db.products.find_one({"_id": ObjectId(product_id)})
    return Product(**updated_product)

@router.delete("/products/{product_id}")
async def delete_product(product_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    result = await db.products.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}