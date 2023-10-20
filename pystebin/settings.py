# ruff: noqa: ANN101, ANN401
import os
import tomllib
from enum import Enum
from pathlib import Path
from typing import Any, Self, Type

from pydantic import Field
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_settings.sources import PydanticBaseSettingsSource


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


class AppSettings(BaseSettings):
    domain: str = "http://localhost:8080/"


class AuthSettings(BaseSettings):
    secret: str
    algorithm: Algorithm = Algorithm.HS256


class GitHubSettings(BaseSettings):
    client_id: str
    client_secret: str


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PYSTEBIN_DATABASE")
    host: str = "localhost"
    database: str = "postgres"
    user: str = "postgres"
    password: str = "password"
    port: int = 5432


class TomlConfigSettingsSource(PydanticBaseSettingsSource):
    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> tuple[Any, str, bool]:
        encoding = self.config.get("env_file_encoding", "utf8")
        file_content_toml = tomllib.loads(
            path.read_text(encoding)
            if (
                path := Path(os.getenv("PYSTEBIN_CONFIG", "/etc/pystebin.toml"))
            ).exists()
            else ""
        )
        field_value = file_content_toml.get(field_name)
        return field_value, field_name, False

    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        return value

    def __call__(self) -> dict[str, Any]:
        d: dict[str, Any] = {}

        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(
                field, field_name
            )
            field_value = self.prepare_field_value(
                field_name, field, field_value, value_is_complex
            )
            if field_value is not None:
                d[field_key] = field_value

        return d


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PYSTEBIN_", env_nested_delimiter="__")
    app: AppSettings = AppSettings()
    auth: AuthSettings
    github: GitHubSettings
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)

    @classmethod
    def settings_customise_sources(
        cls: Type[Self],
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            TomlConfigSettingsSource(settings_cls),
        )
