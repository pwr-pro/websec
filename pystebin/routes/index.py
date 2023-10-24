from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from pystebin.models import CONTENT_TYPE
from pystebin.routes import templates
from pystebin.routes.user import user

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index_get(
    request: Request,
    user: Annotated[dict[str, Any] | None, Depends(user)],
    message: str | None = None,
):
    return templates.TemplateResponse(
        "index.html.j2",
        {
            "request": request,
            "user": user,
            "message": message,
            "content_types": CONTENT_TYPE,
        },
    )
