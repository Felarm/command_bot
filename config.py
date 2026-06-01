from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    USERS_SERVICE_URL: str
    USERS_SERVICE_TOKEN: str
    USERS_REGISTER_ENDPOINT: str = "/register/tg"
    USERS_REFRESH_ENDPOINT: str = "/refresh"

    TASKS_N_NOTES_SERVICE_URL: str


    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()