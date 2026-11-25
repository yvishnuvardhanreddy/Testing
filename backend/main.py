from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
import uuid
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Item API",
    description="CRUD API for managing items",
    version="1.0.0"
)

# CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:8080", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models with validation
class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: Optional[str] = Field(None, max_length=500, description="Item description")
    price: float = Field(..., gt=0, description="Item price (must be positive)")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        v = v.strip()
        if not v:
            raise ValueError('Name cannot be empty or whitespace')
        return v


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: Optional[str] = Field(None, max_length=500, description="Item description")
    price: float = Field(..., gt=0, description="Item price (must be positive)")


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Item name")
    description: Optional[str] = Field(None, max_length=500, description="Item description")
    price: Optional[float] = Field(None, gt=0, description="Item price (must be positive)")


class ItemResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    price: float


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None


class SuccessResponse(BaseModel):
    message: str
    id: Optional[str] = None
    item: Optional[ItemResponse] = None

# In-memory "database"
fake_db: dict[str, dict] = {
    str(uuid.uuid4()): {"name": "Widget", "description": "A nice widget", "price": 9.99},
    str(uuid.uuid4()): {"name": "Gadget", "description": "A cool gadget", "price": 19.99},
}


def validate_item_id(item_id: str) -> dict:
    """Validate item ID exists and return the item, or raise HTTPException."""
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail=f"Item with ID '{item_id}' not found")
    return fake_db[item_id]

# 1. GET endpoint – returns a list of items
@app.get("/items/", response_model=List[ItemResponse])
async def read_items():
    """Get all items in the database."""
    items = list(fake_db.values())
    return [{"id": item_id, **item} for item_id, item in fake_db.items()]


# 2. GET endpoint – get a single item by ID
@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: str):
    """Get a single item by its unique ID."""
    item = validate_item_id(item_id)
    return {"id": item_id, **item}


# 3. POST endpoint – create a new item
@app.post("/items/", response_model=SuccessResponse)
async def create_item(item: ItemCreate):
    """Create a new item with a unique UUID."""
    new_id = str(uuid.uuid4())
    fake_db[new_id] = {
        "name": item.name,
        "description": item.description,
        "price": item.price
    }
    return {
        "message": "Item created successfully",
        "id": new_id,
        "item": {"id": new_id, "name": item.name, "description": item.description, "price": item.price}
    }

# 4. PUT endpoint – update an existing item
@app.put("/items/{item_id}", response_model=SuccessResponse)
async def update_item(item_id: str, item: ItemUpdate):
    """Update an existing item. Only provided fields will be updated."""
    existing_item = validate_item_id(item_id)
    
    # Update only the fields that are provided
    updated_item = {
        "name": item.name if item.name is not None else existing_item["name"],
        "description": item.description if item.description is not None else existing_item["description"],
        "price": item.price if item.price is not None else existing_item["price"]
    }
    
    fake_db[item_id] = updated_item
    return {
        "message": "Item updated successfully",
        "id": item_id,
        "item": {"id": item_id, **updated_item}
    }


# 5. DELETE endpoint – remove an item
@app.delete("/items/{item_id}", response_model=SuccessResponse)
async def delete_item(item_id: str):
    """Delete an item by its unique ID."""
    existing_item = validate_item_id(item_id)
    del fake_db[item_id]
    return {
        "message": "Item deleted successfully",
        "id": item_id
    }

@app.delete_2("/items/{item_id}", response_model=SuccessResponse)
async def delete_item_2(item_id: str):
    """Delete an item by its unique ID."""
    existing_item = validate_item_id(item_id)
    del fake_db[item_id]
    return {
        "message": "Item deleted successfully",
        "id": item_id
    }
    


if __name__ == "__main__":
    uvicorn.run(app, host="localhost",port=8000)