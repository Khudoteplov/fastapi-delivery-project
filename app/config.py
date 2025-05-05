from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_username: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    access_token_expire_minutes: int
    secret_key: str
    algo: str
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
