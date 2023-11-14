import logging
import sys
from typing import Sequence

import psycopg
import pydantic_core
from fastapi import FastAPI, HTTPException, Request

import pystebin.database as database
import pystebin.routes.index as index
import pystebin.routes.paste as paste
import pystebin.routes.user as user
from pystebin.routes import templates
from pystebin.settings import Settings

log = logging.getLogger("pystebin")
log.setLevel(logging.INFO)

app = FastAPI(docs_url=None, redoc_url=None)
app.include_router(index.router)
app.include_router(user.router)
# ! IMPORTANT paste router has to be last
# ! so that it doesn't mask routes
app.include_router(paste.router)

try:
    config: Settings = Settings()  # type: ignore
except pydantic_core.ValidationError as e:
    log.error(e)
    sys.exit(-1)


@app.on_event("startup")
async def startup():
    app.state.config = config
    app.state.db = None
    retry_count = 0
    while app.state.db is None and retry_count < 5:
        try:
            app.state.db = await database.connect(app.state.config.database)
        except psycopg.OperationalError:
            retry_count += 1
            log.warning(f"failed to connect to database retrying [{retry_count}/5]")

    if app.state.db is None:
        log.warning("failed to connect to database exiting")
        sys.exit(-1)
    else:
        await database.init(app.state.db)


@app.exception_handler(401)
async def handle_401(request: Request, exc: HTTPException):
    return templates.TemplateResponse("401.html.j2", {"request": request})


@app.exception_handler(404)
async def handle_404(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "404.html.j2", {"request": request, "page": exc.detail}
    )


def main(argv: Sequence[str] | None = None) -> int:
    import uvicorn

    uvicorn.run(app, host=config.app.host, port=config.app.port, server_header=False)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
