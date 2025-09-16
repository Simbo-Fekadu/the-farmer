from fastapi import FastAPI, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .routers import products

load_dotenv()

app = FastAPI(title="The Farmer API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router, prefix="/api/v1", tags=["products"])

# MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "the_farmer_dev")

client = AsyncIOMotorClient(MONGODB_URI)
db = client[MONGODB_DB_NAME]

class User(BaseModel):
    email: str
    role: str

# Mock auth dependency (replace with real auth validation)
def get_current_user():
    # In production, validate JWT or session from Better-Auth
    return {"email": "user@example.com", "role": "farmer"}

@app.get("/")
async def root():
    return {"message": "Welcome to The Farmer API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/protected")
async def protected_route(user: dict = Depends(get_current_user)):
    return {"message": f"Hello {user['email']}, role: {user['role']}"}

@app.on_event("startup")
async def startup_event():
    # Test MongoDB connection
    try:
        await client.admin.command('ping')
        print("Connected to MongoDB")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    client.close()
    print("Disconnected from MongoDB")