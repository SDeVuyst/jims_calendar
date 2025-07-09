from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Gym Calendar Feed"
    timezone: str = "Europe/Brussels"
    secret_token: str
    jims_email: str
    jims_password: str

    class Config:
        env_file = ".env"

settings = Settings()
