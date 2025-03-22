from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prisma.db import init_db, close_db
from app.api.routes import ping, users, forms, organizations

app = FastAPI(title="BitSH TechX API")

@app.on_event("startup")
async def startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db()

# CORS setup
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(ping.router, prefix="/api", tags=["health"])
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(forms.router, prefix="/api", tags=["forms"])
app.include_router(organizations.router, prefix="/api", tags=["organizations"])

@app.get("/")
def read_root():
    return {"message": "BitSH TechX API is running"}