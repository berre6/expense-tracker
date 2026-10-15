from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    database_url: str

    @property
    def database_path(self):
      prefix = "sqlite:///"
      if not self.database_url.startswith(prefix):
        raise ValueError("Only SQLite database URLs are supported")
      return self.database_url[len(prefix):]

    model_config = ConfigDict(env_file=".env")


settings = Settings()