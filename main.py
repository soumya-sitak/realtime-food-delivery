from bson import ObjectId
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.database import menu_items_collection

app = FastAPI(title="Real-Time Food Delivery API")


class MenuItemCreate(BaseModel):
    name: str
    price: float
    category: str


class MenuItem(BaseModel):
    id: str
    name: str
    price: float
    category: str


def item_from_mongo(item: dict) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "price": item["price"],
        "category": item["category"],
    }


@app.get("/")
def home():
    return {"message": "Food Delivery API is running", "status": "healthy"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/menu-items", response_model=MenuItem)
def create_menu_item(item: MenuItemCreate):
    new_item = {
        "name": item.name,
        "price": item.price,
        "category": item.category,
    }

    result = menu_items_collection.insert_one(new_item)
    saved_item = menu_items_collection.find_one({"_id": result.inserted_id})

    return item_from_mongo(saved_item)


@app.get("/menu-items", response_model=list[MenuItem])
def list_menu_items():
    items = menu_items_collection.find()
    return [item_from_mongo(item) for item in items]


@app.get("/menu-items/{item_id}", response_model=MenuItem)
def get_menu_item(item_id: str):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="Invalid menu item ID")

    item = menu_items_collection.find_one({"_id": ObjectId(item_id)})

    if item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")

    return item_from_mongo(item)
