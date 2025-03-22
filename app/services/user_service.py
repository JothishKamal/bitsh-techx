import hashlib
from prisma.db import prisma

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

async def create_user(email: str, name: str, password: str, metadata=None):
    # Create user
    user = await prisma.user.create(
        data={
            "email": email,
            "name": name,
            "password": hash_password(password)
        }
    )
    
    # Add metadata if provided
    if metadata:
        for key, value in metadata.items():
            await prisma.usermetadata.create(
                data={
                    "user_id": user.id,
                    "key": key,
                    "value": value
                }
            )
    
    return user

async def get_user(user_id: int):
    return await prisma.user.find_unique(
        where={"id": user_id},
        include={"userMetadata": True}
    )