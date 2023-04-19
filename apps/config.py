from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER_NAME: str
    DB_PWD: str
    SIGN_KEY: str
    SIGN_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTE: int

    class Config:
        env_file = ".env"  # source the .env variable file.


settings = Settings()
