from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_users():
    return [{"username": "user1"}, {"username": "user2"}]
