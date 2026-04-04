from app.infrastructure.database.session import SessionLocal
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_service(service_class, repo_class):
    def _get_service(db=Depends(get_db)):
        repo = repo_class(db)
        return service_class(repo)
    return _get_service