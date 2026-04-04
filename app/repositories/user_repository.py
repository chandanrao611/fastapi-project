from sqlalchemy.orm import Session
from app.infrastructure.database.base_repository import BaseRepository
from app.models.user_model import User


class UserRepository(BaseRepository[User]):

    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()