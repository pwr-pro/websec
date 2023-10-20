import psycopg

from pystebin.settings import DatabaseSettings


async def connect(config: DatabaseSettings):
    con = await psycopg.AsyncConnection.connect(
        f"postgresql://{config.user}@{config.host}:{config.port}/{config.database}"
    )
    async with con.cursor() as cur:
        await cur.execute("select version()")
        version = await cur.fetchone()
        print(f"Connected with: {version[0]}") if version else None
    return con


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
