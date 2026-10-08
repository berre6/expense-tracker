from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    database_url: str

    @property
    def database_path(self):
        return self.database_url.replace("sqlite:///", "")

    model_config = ConfigDict(env_file=".env")


settings = Settings()