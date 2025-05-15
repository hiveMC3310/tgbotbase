from enum import StrEnum, auto
from pathlib import Path

import tomlkit
from pydantic import BaseModel, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

configs_path = Path(__file__).parent


class LogRenderer(StrEnum):
    JSON = auto()
    CONSOLE = auto()


class BotSettings(BaseModel):
    token: SecretStr
    admins: list[int]


class LogSettings(BaseModel):
    show_datetime: bool
    datetime_format: str
    level: str
    use_colors_in_console: bool
    renderer: LogRenderer
    path: Path

    @field_validator('renderer', mode="before")
    @classmethod
    def log_renderer_to_lower(cls, v: str):
        return v.lower()


class Settings(BaseSettings):
    bot: BotSettings
    log: LogSettings

    model_config = SettingsConfigDict(
        env_file=configs_path / ".env",
        env_nested_delimiter="__",
        extra="ignore"
    )

    @classmethod
    def from_toml(cls, path: Path) -> "Settings":
        toml_path = configs_path / Path(path).resolve()
        if not toml_path.exists():
            raise FileNotFoundError(f"Config file {path} not found")

        config_data = {}
        with open(toml_path, "r", encoding="utf-8") as f:
            toml_data = tomlkit.parse(f.read())
            config_data["log"] = toml_data.get("log", {})

        return cls(**config_data)
