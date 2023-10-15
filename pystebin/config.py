import os
import tomllib
from enum import Enum
from pathlib import Path
from typing import Any, Self

from pydantic import BaseModel, Field


class Algorithm(str, Enum):
    HS256 = "HS256"
    HS384 = "HS384"
    HS512 = "HS512"
    RS256 = "RS256"
    RS384 = "RS384"
    RS512 = "RS512"
    ES256 = "ES256"
    ES384 = "ES384"
    ES512 = "ES512"


class AppConfig(BaseModel):
    domain: str


class AuthConfig(BaseModel):
    secret: str
    algorithm: Algorithm = Algorithm.HS256


class GHConfig(BaseModel):
    client_id: str
    client_secret: str


class DBConfig(BaseModel):
    host: str = "localhost"
    database: str = "postgres"
    user: str = "postgres"
    password: str = "password"
    port: int = 5432


class Config(BaseModel):
    app: AppConfig
    auth: AuthConfig
    github: GHConfig
    db: DBConfig = Field(default_factory=DBConfig)

    @classmethod
    def from_dict(cls: type[Self], dict: dict[str, Any]) -> Self:
        return cls(
            github=GHConfig(**dict.get("github", {})),
            db=DBConfig(**dict.get("db", {})),
            app=AppConfig(**dict.get("pystebin", {})),
            auth=AuthConfig(**dict.get("auth", {})),
        )


CONFIG_PATH = Path(os.getenv("PYSTEBIN_CONFIG", "/etc/pystebin.toml"))


def read_config():
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open("rb") as f:
            _cfg = tomllib.load(f)
            return Config.from_dict(_cfg)

    else:
        raise FileNotFoundError("couldn't find required config")
