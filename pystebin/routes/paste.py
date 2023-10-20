from typing import TYPE_CHECKING, Annotated, Any

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from psycopg.rows import class_row

from pystebin.models.paste import CONTENT_TYPE, PasteList, PasteView
from pystebin.routes import templates
from pystebin.routes.user import authorized, user

if TYPE_CHECKING:
    import psycopg
    from psycopg import AsyncConnection

router = APIRouter()


@router.get("/list")
async def list_pastes(
    request: Request,
    user: Annotated[dict[str, Any] | None, Depends(user)],
):
    if user is None:
        return templates.TemplateResponse(
            "index.html.j2",
            {"request": request, "user": user, "message": "Unauthorized!"},
        )

    db: AsyncConnection = request.app.state.db

    async with db.cursor(row_factory=class_row(PasteList)) as cur:
        await cur.execute("select id, title, content, creation_time from pastes;")
        pastes = await cur.fetchall()

    return templates.TemplateResponse(
        "list.html.j2", {"request": request, "user": user, "pastes": pastes}
    )


@router.post("/")
async def post_paste(
    request: Request,
    user: Annotated[dict[str, Any] | None, Depends(user)],
    title: Annotated[str, Form()],
    content: Annotated[str, Form()],
    content_type: Annotated[str, Form(alias="content-type")] = CONTENT_TYPE.Plaintext,
):
    if user is None:
        return RedirectResponse("/", 302)
    db: psycopg.AsyncConnection = request.app.state.db
    async with db.cursor() as cur:
        await cur.execute(
            """--sql
            insert into pastes
                (author_id, title, content_type, content)
            values ( %s, %s, %s, %s)
            returning id;
            """,
            (user["id"], title, content_type, content),
        )
        await db.commit()
        _id = await cur.fetchone()
        if (id := _id) is None:
            return RedirectResponse("/", 302)

        return RedirectResponse(f"/{id[0]}", 302)


@router.get("/{id:int}")
async def get_paste(
    request: Request,
    id: int,
    user: Annotated[dict[str, Any] | None, Depends(user)],
):
    db: AsyncConnection = request.app.state.db
    async with db.cursor(row_factory=class_row(PasteView)) as cur:
        await cur.execute(
            """--sql
            select id, title, content_type, content, author_id
            from pastes
            where id = %s;
            """,
            (id,),
        )
        post = await cur.fetchone()
        if post is None:
            return templates.TemplateResponse(
                "404.html.j2", {"request": request, "page": id}
            )

    return templates.TemplateResponse(
        "paste.html.j2", {"request": request, "user": user, "p": post}
    )


@router.get("/delete/{id:int}")
async def delete_paste(
    request: Request,
    id: int,
    user: Annotated[dict[str, Any], Depends(authorized)],
):
    db: AsyncConnection = request.app.state.db
    async with db.cursor() as cur:
        await cur.execute(
            "delete from pastes where id = %s and author_id = %s",
            (id, user["id"]),
        )
        await db.commit()
        return RedirectResponse("/list", 302)


@router.get("/{page}")
async def redirect(request: Request, page: Any):  # noqa: ANN401
    return templates.TemplateResponse("404.html.j2", {"request": request, "page": page})
