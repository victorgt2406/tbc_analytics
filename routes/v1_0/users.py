# Ejemplo de users.py en v1.0, v1.1, y beta
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_users():
    return {"message": "Lista de usuarios para versión específica en v1_0"}
