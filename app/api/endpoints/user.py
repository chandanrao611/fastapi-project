from fastapi import APIRouter, Depends, Query
from app.api.deps import get_service
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.schemas.PaginatedData import PaginatedData
from app.schemas.ResponseModel import ResponseModel
from app.schemas.user import UserResponse, UserCreate, UserUpdate
from app.utils.Response import Response
from app.core.status import HTTPStatus

router = APIRouter()

@router.get("/", response_model=ResponseModel[PaginatedData[UserResponse]])
def getUsers(page: int = 1, size: int = 10, service: UserService = Depends(get_service(UserService, UserRepository))):
    data = service.get_users_paginated(page, size)
    return Response.success(data, "User list retrieved successfully")

@router.get("/profile/{user_id}", response_model=ResponseModel[UserResponse])
def getUserProfile(user_id: int, service: UserService = Depends(get_service(UserService, UserRepository))):
    data = service.get_user(user_id)
    return Response.success(data, "User profile retrieved successfully")

@router.post("/register", response_model=ResponseModel[UserResponse])
def createUser(user_data: UserCreate, service: UserService = Depends(get_service(UserService, UserRepository))):
    data = service.create_user(user_data)
    return Response.success(data, "User created successfully", status_code=HTTPStatus.CREATED)

@router.put("/update", response_model=ResponseModel[UserResponse])
def updateUser(user_data: UserUpdate, user_id: int = Query(..., gt=0, description="User ID must be positive"), service: UserService = Depends(get_service(UserService, UserRepository))):
    data = service.update_user(user_id, user_data)
    return Response.success(data, "User updated successfully")