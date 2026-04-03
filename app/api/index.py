from fastapi import APIRouter
from app.api import user

router = APIRouter()

# Including the all the routers with their respective prefixes and tags
# api_router.include_router(auth.router, prefix="/", tags=["Auth"])
router.include_router(user.router, prefix="/user", tags=["User"])