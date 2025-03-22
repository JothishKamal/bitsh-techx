from fastapi import APIRouter, HTTPException
from app.api.models.users import UserCreate, User
from app.services import user_service
from app.db import prisma  # Import prisma object

router = APIRouter()

@router.post("/users", response_model=User)
async def create_user(user_data: UserCreate):
    # Check if user exists
    existing_user = await prisma.user.find_unique(
        where={"email": user_data.email}
    )
    
    if existing_user:
        raise HTTPException(
            status_code=400, 
            detail="User with this email already exists"
        )
    
    user = await user_service.create_user(
        user_data.email,
        user_data.name,
        user_data.password,
        user_data.metadata
    )
    
    return user

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = await user_service.get_user(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user