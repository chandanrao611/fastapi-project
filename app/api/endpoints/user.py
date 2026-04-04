from fastapi import APIRouter
from app.schemas.PaginatedData import PaginatedData
from app.schemas.ResponseModel import ResponseModel
from app.schemas.user import UserCreate
from app.utils.Response import Response
from app.core.status import HTTPStatus
from fastapi import Depends
from app.api.deps import get_service
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository

router = APIRouter()

@router.get("/", response_model=ResponseModel[PaginatedData[dict]])
def getUsers(page: int = 1, size: int = 10, service: UserService = Depends(get_service(UserService, UserRepository))):
    data = service.get_users_paginated(page, size)
    return Response.success(data, "User list retrieved successfully")

@router.get("/profile/{user_id}")
def getUserProfile(user_id: int, service: UserService = Depends(get_service(UserService, UserRepository))):
    data = service.get_user(user_id)
    return Response.success(data, "User profile retrieved successfully")

@router.post("/register")
def createUser(user_data: UserCreate, service: UserService = Depends(get_service(UserService, UserRepository))):
    data = service.create_user(user_data)
    return Response.success(data, "User created successfully", status_code=HTTPStatus.CREATED)