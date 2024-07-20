from pydantic_settings import BaseSettings
from pydantic.networks import PostgresDsn, AnyUrl


class Settings(BaseSettings):
    POSTGRES_URL: PostgresDsn
    ACCESS_TOKEN_SECRET: str
    REFRESH_TOKEN_SECRET: str
    RESET_PASSWORD_SECRET: str

    SECRET_KEY: str  # Secret key or Its Dangerous

    REDIS_HOST: str
    REDIS_PORT: int

    JWT_ALGORITHM: str

    AWS_SECRET_KEY: str
    AWS_ACCESS_KEY: str
    BUCKET_NAME: str
    AWS_REGION: str

    CLOUD_FRONT_URL: AnyUrl

    class Config:
        env_file = ".env"
