# app/routers/user.py

from fastapi import APIRouter
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
