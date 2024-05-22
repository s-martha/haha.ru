from pydantic_settings import BaseSettings, SettingsConfigDict
import os
class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    SECRET_KEY: str
    # @property
    # def DATABASE_URL_psycopg(self):
    #     return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def SecretKey(self):
        return self.SECRET_KEY

    model_config = SettingsConfigDict(env_file=".env")

setting = Settings()