import logging
from datetime import datetime

import psycopg

from pystebin.config import DBConfig, read_config
from pystebin.models.paste import CONTENT_TYPE, Paste

db_test = (
    Paste(
        id=1,
        title="Hello",
        content="aaaAAaaa...",
        content_type=CONTENT_TYPE.Plaintext,
        creation_time=datetime(2020, 10, 1),
        author_id=79099832,
    ),
    Paste(
        id=3,
        title="Hello DIR SIR AAOMIMIKASNDIASDOASNDIASNDASNDOASD",
        content="aaaAAaaa..." * 50,
        content_type=CONTENT_TYPE.Plaintext,
        creation_time=datetime(2020, 10, 1),
        author_id=79099832,
    ),
    Paste(
        id=4,
        title="Hello",
        content="aaaAAaaa...",
        content_type=CONTENT_TYPE.Plaintext,
        creation_time=datetime(2020, 10, 1),
        author_id=79099832,
    ),
    Paste(
        id=3,
        title="Hello",
        content="aaaAAaaa...",
        content_type=CONTENT_TYPE.Plaintext,
        creation_time=datetime(2020, 10, 1),
        author_id=79099832,
    ),
)


def get(id: int) -> Paste | None:
    for p in db_test:
        if p.id == id:
            return p

    return None


async def connect(config: DBConfig):
    con = await psycopg.AsyncConnection.connect(
        f"postgresql://{config.user}@{config.host}:{config.port}/{config.database}"
    )
    async with con.cursor() as cur:
        await cur.execute("select version()")
        version = await cur.fetchone()
        print(f"Connected with: {version[0]}") if version else None
    return con


async def db():
    config = read_config()
    _db = await connect(config.db)
    logging.warning("getting db connection")
    try:
        yield _db
    finally:
        await _db.close()

async def init(con: psycopg.AsyncConnection):
    async with con.cursor() as cur:
        await cur.execute(
            """--sql
            create table if not exists pastes (
                    id serial primary key,
                    author_id integer not null,
                    title varchar(128) not null,
                    content_type varchar(32) not null default 'text/plain',
                    content text not null,
                    creation_time timestamp default now()
                );
                """
        )
        await con.commit()
