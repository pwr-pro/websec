from fastapi.exceptions import HTTPException


class UnauthorizedException(HTTPException):
    pass
