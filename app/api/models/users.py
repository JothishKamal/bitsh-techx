from pydantic import BaseModel, EmailStr
from typing import Dict, Any, Optional, List

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str
    metadata: Optional[Dict[str, Any]] = None

class UserMetadataCreate(BaseModel):
    key: str
    value: Dict[str, Any]

class UserMetadata(UserMetadataCreate):
    id: int
    userId: int
    
    class Config:
        from_attributes = True

class User(UserBase):
    id: int
    userMetadata: List[UserMetadata] = []
    
    class Config:
        from_attributes = True