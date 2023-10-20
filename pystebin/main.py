from typing import Sequence

from fastapi import FastAPI, Request

import pystebin.database as database
import pystebin.routes.index as index
import pystebin.routes.paste as paste
import pystebin.routes.user as user
from pystebin.exception import UnauthorizedException
from pystebin.routes import templates
from pystebin.settings import Settings

app = FastAPI(docs_url=None, redoc_url=None)
app.include_router(index.router)
app.include_router(user.router)
# ! IMPORTANT paste router has to be last
# ! so that it doesn't mask routes
app.include_router(paste.router)


@app.on_event("startup")
async def startup():
    app.state.config: Settings = Settings()  # type: ignore
    app.state.db = await database.connect(app.state.config.database)
    await database.init(app.state.db)


@app.exception_handler(UnauthorizedException)
async def unauthorized_handler(request: Request, exc: UnauthorizedException):
    return templates.TemplateResponse("401.html.j2", {"request": request})


def main(argv: Sequence[str] | None = None) -> int:
    import uvicorn

    uvicorn.run(app)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
