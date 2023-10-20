import json
from typing import TYPE_CHECKING, Annotated, Any

import httpx
from fastapi import Cookie, Depends, Form, HTTPException, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter
from jose import JWSError, jws

from pystebin.routes import templates

if TYPE_CHECKING:
    from psycopg import AsyncConnection

    from pystebin.settings import Settings


router = APIRouter()


async def get_user_data(access_token: str) -> dict[str, Any]:
    async with httpx.AsyncClient() as c:
        response = await c.get(
            url="https://api.github.com/user",
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {access_token}",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        return response.json()


async def user(
    requset: Request,
    access_token: str | None = Cookie(default=None),
) -> dict[str, Any] | None:
    config: Settings = requset.app.state.config
    if access_token:
        try:
            result = jws.verify(
                access_token, key=config.auth.secret, algorithms=[config.auth.algorithm]
            )
            return json.loads(result)
        except JWSError:
            return None
    else:
        return None


def authorized(user: Annotated[dict[str, Any], Depends(user)]):
    if user:
        return user
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)


@router.get("/login")
async def login(request: Request, code: str | None = None):
    config: Settings = request.app.state.config
    if code is None:
        return RedirectResponse(
            f"https://github.com/login/oauth/authorize?client_id={config.github.client_id}",
            status_code=302,
        )

    async with httpx.AsyncClient() as c:
        r = await c.post(
            url="https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            params={
                "client_id": config.github.client_id,
                "client_secret": config.github.client_secret,
                "code": code,
            },
        )
    github_token: dict[str, Any] = r.json()
    if github_token.get("error") is not None:
        return RedirectResponse(
            f"{config.pystebin.domain}/", status_code=status.HTTP_400_BAD_REQUEST
        )
    response = RedirectResponse(
        f"{config.pystebin.domain}/", status_code=status.HTTP_303_SEE_OTHER
    )
    access_token = github_token["access_token"]
    github_user = await get_user_data(access_token)
    cookie = jws.sign(
        payload={
            "access_token": access_token,
            "id": github_user["id"],
            "login": github_user["login"],
        },
        key=config.auth.secret,
        algorithm=config.auth.algorithm,
    )
    response.set_cookie(
        key="access_token",
        value=cookie,
        httponly=True,
        secure=True,
    )
    return response


@router.get("/settings")
async def settings(
    request: Request,
    user: Annotated[dict[str, Any], Depends(authorized)],
):
    return templates.TemplateResponse(
        "settings.html.j2",
        {
            "request": request,
            "user": user,
        },
    )


@router.get("/logout")
async def logout(
    request: Request,
    user: Annotated[dict[str, Any], Depends(authorized)],
):
    config: Settings = request.app.state.config
    if user is None:
        return RedirectResponse(f"{config.pystebin.domain}/", status.HTTP_302_FOUND)
    response = templates.TemplateResponse(
        "index.html.j2",
        {"request": request, "user": None, "message": "Successfully logged out!"},
    )
    response.delete_cookie("access_token")
    return response


@router.get("/delete")
async def delete(
    request: Request,
    user: Annotated[dict[str, Any], Depends(authorized)],
    confirm: Annotated[bool, Form()] = False,
):
    config: Settings = request.app.state.config
    if user is None:
        return RedirectResponse(f"{config.pystebin.domain}/", status.HTTP_302_FOUND)

    if confirm is False:
        return templates.TemplateResponse(
            "settings.html.j2",
            {
                "request": request,
                "user": user,
                "message": "No confirmation received :(",
            },
        )
    else:
        db: AsyncConnection = request.app.state.db
        async with db.cursor() as cur:
            await cur.execute("""delete from pastes where author_id = %s;""")
            await db.commit()
        response = templates.TemplateResponse(
            "index.html.j2",
            {
                "request": request,
                "user": None,
                "message": "Account successfully deleted!",
            },
        )
        response.delete_cookie("access_token")

        return response
