from fastapi.responses import JSONResponse
from app.core.status import HTTPStatus
class Response:
    @staticmethod
    def success(data=None, message="Success", status_code=HTTPStatus.SUCCESS):
        return JSONResponse(
            status_code=status_code,
            content={
                "message": message,
                "status": "success",
                "data": data
            }
        )

    @staticmethod
    def error(message="Error", data=None, status_code=HTTPStatus.BAD_REQUEST):
        return JSONResponse(
            status_code=status_code,
            content={
                "message": message,
                "status": "error",
                "data": data
            }
        )