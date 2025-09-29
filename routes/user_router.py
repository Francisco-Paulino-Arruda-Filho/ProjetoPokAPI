from bson import ObjectId
from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from database import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, users_collection
from models.User import UserCreate
from models.UserLogin import UserLogin
import bcrypt
import jwt
from bson.binary import Binary
from database import pokemons_collection

user_router = APIRouter()

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@user_router.post("/register")
async def register(user: UserCreate):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário já existe.")
    
    hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    await users_collection.insert_one({
        "username": user.username,
        "email": user.email,
        "password": hashed_pw
    })
    return {"msg": "Usuário criado com sucesso."}

@user_router.delete("/user/{user_id}")
async def delete_user(user_id: str):
    try:
        obj_id = ObjectId(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID inválido.")

    result = await users_collection.delete_one({"_id": obj_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    await pokemons_collection.delete_many({"user_id": obj_id})

    return {"msg": "Usuário e seus times associados foram excluídos com sucesso."}

@user_router.post("/login")
async def login(user: UserLogin):
    db_user = await users_collection.find_one({"email": user.username})
    if not db_user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")

    stored_password = db_user["password"]

    if isinstance(stored_password, Binary):
        stored_password = bytes(stored_password)

    if not bcrypt.checkpw(user.password.encode('utf-8'), stored_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")

    user_id = str(db_user["_id"])  
    username = db_user["username"]
    token = create_token({"sub": db_user["username"], "id": user_id})
    email = db_user.get("email", None)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user_id,
        "username": username,
        "email": email
    }

