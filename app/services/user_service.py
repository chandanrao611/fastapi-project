from fastapi import HTTPException
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.schemas.PaginatedData import PaginatedData
from app.schemas.ResponseModel import ResponseModel
from app.schemas.user import UserResponse, UserCreate
from app.utils.helper import map_to_schema
from app.core.security import hash_password
from app.core.status import HTTPStatus

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_user(self, user_id: int):
        data = self.repo.db.query(User).filter(User.id == user_id).first()
        if not data:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
        return UserResponse.model_validate(data)

    def get_all_users(self):
        return self.repo.db.query(User).all()

    def get_users_paginated(self, page: int, size: int):
        users, total = self.repo.get_paginated(
            page=page,
            size=size
        )
        user_list = map_to_schema(UserResponse, users)
        
        return PaginatedData(
            items=user_list,
            page=page,
            size=size,
            total=total
        )

    def create_user(self, user_data: UserCreate):
        if self.repo.get_by_email(user_data.email):
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Email already exists")

        user_data.password = hash_password(user_data.password)
        user = self.repo.create(user_data)
        return UserResponse.model_validate(user)