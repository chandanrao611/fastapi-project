from fastapi import APIRouter
from app.schemas.PaginatedData import PaginatedData
from app.schemas.ResponseModel import ResponseModel
from app.utils.Response import Response
from app.core.status import HTTPStatus

router = APIRouter()

@router.post("/login", response_model=ResponseModel[PaginatedData[dict]])
def login():
    # Placeholder for login logic
    pass

@router.post("/otp")
def getOTP(user_id: int):
    if user_id != 1:
        return Response.error("User not found", status_code=HTTPStatus.NOT_FOUND)
    data = {"id": user_id, "name": "John Doe"}
    return Response.success(data, "User profile retrieved successfully")

@router.post("/validate-otp")
def validateOTP(user_id: int):
    if user_id != 1:
        return Response.error("User not found", status_code=HTTPStatus.NOT_FOUND)
    data = {"id": user_id, "name": "John Doe"}
    return Response.success(data, "User profile retrieved successfully")

@router.post("/reset-password")
def resetPassword(user_id: int):
    if user_id != 1:
        return Response.error("User not found", status_code=HTTPStatus.NOT_FOUND)
    data = {"id": user_id, "name": "John Doe"}
    return Response.success(data, "User profile retrieved successfully")

@router.post("/forgot-password")
def forgotPassword(user_id: int):
    if user_id != 1:
        return Response.error("User not found", status_code=HTTPStatus.NOT_FOUND)
    data = {"id": user_id, "name": "John Doe"}
    return Response.success(data, "User profile retrieved successfully")