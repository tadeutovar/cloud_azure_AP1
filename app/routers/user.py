# app/routers/user.py

from fastapi import APIRouter, HTTPException
from app.database import client
from app.models.user import User
from app.models.card import Card
from bson import ObjectId

router = APIRouter()

# Rota para criar um usuário
@router.post("/users/")
async def create_user(user: User):
    users_collection = client.db.users
    user_dict = user.dict()
    result = users_collection.insert_one(user_dict)
    return {"id": str(result.inserted_id)}

def serialize_user(user):
    user["_id"] = str(user["_id"])
    return user

@router.get("/users/")
async def get_all_users():
    users_collection = client.db.users
    users = list(users_collection.find())

    # Converter todos os `_id` para string antes de retornar
    return [serialize_user(user) for user in users]

@router.get("/users/{user_id}")
async def get_user_by_id(user_id: str):
    users_collection = client.db.users
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return serialize_user(user)

users_collection = client.db.users

# Atualizar Usuário
@router.put("/users/{user_id}")
async def update_user(user_id: str, user_data: dict):
    if not users_collection.find_one({"_id": ObjectId(user_id)}):
        raise HTTPException(status_code=404, detail="User not found")

    users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": user_data})
    return {"message": "User updated successfully"}

# Deletar Usuário
@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}