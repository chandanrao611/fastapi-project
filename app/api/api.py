from fastapi import APIRouter
from app.api.endpoints import user, auth, health

router = APIRouter()

# Including all routers with respective prefixes and tags
# Do not use trailing slash on prefix (FastAPI disallows endpoint prefixes ending in '/')
router.include_router(auth.router, prefix="", tags=["Auth"])
router.include_router(user.router, prefix="/user", tags=["User"])
router.include_router(health.router, prefix="/health", tags=["Health"])