from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.api.deps import get_db

router = APIRouter()


@router.get("/db")
def check_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "message": "Database connected",
            "status": "success",
            "data": None
        }
    except Exception as e:
        return {
            "message": str(e),
            "status": "error",
            "data": None
        }