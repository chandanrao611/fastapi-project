from fastapi import APIRouter, Depends, Query, UploadFile, File
from fastapi.responses import StreamingResponse, HTMLResponse

from app.api.deps import get_service
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.schemas.PaginatedData import PaginatedData
from app.schemas.ResponseModel import ResponseModel
from app.schemas.user import UserResponse, UserCreate, UserUpdate
from app.utils.Response import Response
from app.core.status import HTTPStatus
from app.services.pdf_service import PDFService

router = APIRouter()


def _sample_invoice():
    #Return a small sample invoice payload used by the example PDF/html endpoints.#
    return {
        "customer_name": "John Doe",
        "items": [
            {"name": "Laptop", "price": 50000},
            {"name": "Mouse", "price": 1000},
        ],
    }

#List users (paginated).
@router.get("/", response_model=ResponseModel[PaginatedData[UserResponse]])
def get_users(page: int = 1, size: int = 10, service: UserService = Depends(get_service(UserService, UserRepository))):
    data = service.get_users_paginated(page, size)
    return Response.success(data, "User list retrieved successfully")

#Get a single user by ID.#
@router.get("/profile/{user_id}", response_model=ResponseModel[UserResponse])
def get_user_profile(user_id: int, service: UserService = Depends(get_service(UserService, UserRepository))):
    data = service.get_user(user_id)
    return Response.success(data, "User profile retrieved successfully")

#Create a new user.#
@router.post("/register", response_model=ResponseModel[UserResponse], status_code=HTTPStatus.CREATED)
def create_user(user_data: UserCreate, service: UserService = Depends(get_service(UserService, UserRepository))):
    data = service.create_user(user_data)
    return Response.success(data, "User created successfully", status_code=HTTPStatus.CREATED)

#Update an existing user by query param `user_id`.#
@router.put("/update", response_model=ResponseModel[UserResponse])
def update_user(user_data: UserUpdate, user_id: int = Query(..., gt=0, description="User ID must be positive"), service: UserService = Depends(get_service(UserService, UserRepository))):
    data = service.update_user(user_id, user_data)
    return Response.success(data, "User updated successfully")

#Bulk upload users from a CSV file.#
@router.post("/upload", response_model=ResponseModel[UserResponse])
def upload_csv(file: UploadFile = File(...), service: UserService = Depends(get_service(UserService, UserRepository))):
    data = service.bulk_upload_users(file)
    return Response.success(data, "Users uploaded successfully")

#Return a generated PDF (example). Not a JSON response.#
@router.get("/view-pdf")
def view_pdf():
    pdf_buffer = PDFService.generate_invoice_pdf(_sample_invoice())
    return StreamingResponse(pdf_buffer, media_type="application/pdf")

#Return a rendered HTML template (example).#
@router.get("/view", response_class=HTMLResponse)
def view_template():
    html = PDFService.generate_template(_sample_invoice())
    return HTMLResponse(content=html)