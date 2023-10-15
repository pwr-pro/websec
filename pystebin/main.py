import logging
import sys
from typing import Sequence

from fastapi import FastAPI, Request

import pystebin.database as database
import pystebin.routes.index as index
import pystebin.routes.paste as paste
import pystebin.routes.user as user
from pystebin.config import read_config
from pystebin.exception import UnauthorizedException
from pystebin.routes import templates

try:
    config = read_config()

except FileNotFoundError:
    logging.fatal("config file not found")
    raise SystemExit(-1)

app = FastAPI(docs_url=None, redoc_url=None)
app.include_router(index.router)
app.include_router(user.router)
# ! IMPORTANT paste router has to be last
# ! so that it doesn't mask routes
app.include_router(paste.router)


@app.on_event("startup")
async def startup():
    app.state.db = await database.connect(config.db)
    app.state.config = read_config()
    await database.init(app.state.db)


@app.exception_handler(UnauthorizedException)
async def unauthorized_handler(request: Request, exc: UnauthorizedException):
    return templates.TemplateResponse("401.html.j2", {"request": request})


def main(argv: Sequence[str] | None = sys.argv[1:]) -> int:
    import uvicorn

    uvicorn.run(app)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
