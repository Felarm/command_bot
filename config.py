from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    USERS_SERVICE_URL: str
    USERS_SERVICE_TOKEN: str
    USERS_REGISTER_ENDPOINT: str = "/auth/register/tg"
    USERS_REFRESH_ENDPOINT: str = "/auth/refresh"
    USERS_LOGIN_ENDPOINT: str = "/auth/login/tg"

    TASKS_N_NOTES_SERVICE_URL: str
    GET_ALL_NOTES_ENDPOINT: str = "/notes"
    CREATE_NOTE_ENDPOINT: str = "/notes"
    DELETE_NOTE_ENDPOINT: str = "/notes/{}"

    CREATE_TASK_ENDPOINT: str = "/tasks"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()