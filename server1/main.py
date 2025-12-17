from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import json
import os

# ==========================================================
# Json handlers:
# ==========================================================

DB_PATH = Path("db/shopping_list.json")

def ensure_database_exists():
    if not Path(DB_PATH).is_file():
        with open(DB_PATH, "w") as file:
            json.dump([], file, indent=2)
            
def load_database():
    ensure_database_exists()
    with open(DB_PATH, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []
        
def save_database(data):
    ensure_database_exists()
    with open(DB_PATH, "w") as file:
        json.dump(data, file, indent=2)

# ==========================================================
# Models:
# ==========================================================

class Item(BaseModel):
    name: str
    quantity: int

# ==========================================================
# App endpoints:
# ==========================================================

app = FastAPI()

@app.get("/")
def home():
    return {"msg": "Welcome to server1!"}

@app.get("/items")
def get_all_items():
    db = load_database()
    return db

@app.post("/items")
def add_item(item: Item):
    db = load_database()
    new_item = item.dict()
    new_item["id"] = str(len(db) + 1)
    db.append(new_item)
    save_database(db)
    return {
        "message": "Item created successfully",
        "item": new_item
    }