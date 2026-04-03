from fastapi import APIRouter
from app.schemas.PaginatedData import PaginatedData
from app.schemas.ResponseModel import ResponseModel
from app.utils.Response import Response
from app.core.status import HTTPStatus

router = APIRouter()

@router.get("/", response_model=ResponseModel[PaginatedData[dict]])
def getUsers():
    data = PaginatedData(items=[{"id": 1, "name": "John Doe"}], page=1, size=10, total=1)
    return Response.success(data, "User list retrieved successfully")

@router.get("/profile/{user_id}")
def getUserProfile(user_id: int):
    if user_id != 1:
        return Response.error("User not found", status_code=HTTPStatus.NOT_FOUND)
    data = {"id": user_id, "name": "John Doe"}
    return Response.success(data, "User profile retrieved successfully")