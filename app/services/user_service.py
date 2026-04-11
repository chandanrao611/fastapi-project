from fastapi import HTTPException
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.schemas.PaginatedData import PaginatedData
from app.schemas.ResponseModel import ResponseModel
from app.schemas.user import UserResponse, UserCreate, UserUpdate
from app.utils.helper import map_to_schema, validate_password, validate_email, validate_mobile
from app.core.security import hash_password
from app.core.status import HTTPStatus
from app.services.file_service import FileService

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    # Validation and processing methods for email
    def _validate_and_process_email(self, email: str):
        email = email.strip().lower()
        error = validate_email(email)
        if error:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=error)
        return email

    # Validation and processing methods for password
    def _validate_and_process_password(self, password: str):
        password = password.strip()
        error = validate_password(password)
        if error:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=error)
        return hash_password(password)
    
    # Validation method for mobile number
    def _validate_mobile(self, mobile: int):
        error = validate_mobile(mobile)
        if error:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=error)
        return mobile

    # Get user data based on user ID
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
        user_data.email = self._validate_and_process_email(user_data.email)

        if self.repo.get_by_email(user_data.email):
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Email already exists")

        if user_data.mobile is not None:
            user_data.mobile = self._validate_mobile(user_data.mobile)

        user_data.password = self._validate_and_process_password(user_data.password)

        user = self.repo.create(user_data)
        return UserResponse.model_validate(user)
    
    def update_user(self, user_id: int, user_data: UserUpdate):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

        if user_data.mobile is not None:
            user_data.mobile = self._validate_mobile(user_data.mobile)

        if user_data.email is not None:
            user_data.email = self._validate_and_process_email(user_data.email)
            if user.email != user_data.email and self.repo.get_by_email(user_data.email):
                raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Email already exists")
        
        if user_data.password is not None:
            user_data.password = self._validate_and_process_password(user_data.password)
            
        user = self.repo.update(user_id, user_data.model_dump(exclude_unset=True))
        return UserResponse.model_validate(user)
    
    def bulk_upload_users(self, file):
        total_rows = FileService.count_rows_binary(file)
        users_stream = FileService.read_file(file)
        
        existing_emails = set(user.email for user in self.repo.db.query(User.email).all())
        
        inserted_users_count = 0
        duplicate_users = []

        batch = []
        BATCH_SIZE = 500
        # Process users in batches to optimize DB inserts
        for row in users_stream:
            try:
                row["email"] = self._validate_and_process_email(row["email"])
                if "mobile" in row and row["mobile"]:
                    row["mobile"] = self._validate_mobile(row["mobile"])
                if "password" in row and row["password"]:
                    row["password"] = self._validate_and_process_password(row["password"])
                
                batch.append(row)
                # Insert batch
                if len(batch) == BATCH_SIZE:
                    inserted, duplicates = self.repo._insert_batch(batch, unique_field="email")
                    inserted_users_count += inserted
                    duplicate_users.extend(duplicates)
                    batch.clear()

            except Exception as e:
                print(f"Error processing row: {e}")
                continue


        # Insert remaining
        if batch:
            inserted, duplicates = self.repo._insert_batch(batch, unique_field="email")
            inserted_users_count += inserted
            duplicate_users.extend(duplicates)

        return {
            "inserted": inserted_users_count,
            "skipped": total_rows - inserted_users_count,
            "duplicate_users": duplicate_users
        }