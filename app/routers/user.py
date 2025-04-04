from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.mysql import get_db
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, UserOut

router = APIRouter()

# Criar usuário (verifica e-mail único)
@router.post("/users/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = UserModel(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Buscar todos os usuários
@router.get("/users/", response_model=list[UserOut])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(UserModel).all()

# Buscar usuário por ID
@router.get("/users/{user_id}", response_model=UserOut)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Atualizar usuário
@router.put("/users/{user_id}")
def update_user(user_id: int, user_data: dict, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_data.items():
        setattr(user, key, value)
    db.commit()
    return {"message": "User updated successfully"}

# Deletar usuário
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
