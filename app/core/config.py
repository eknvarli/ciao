from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Ciao Music API"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    SQLALCHEMY_DATABASE_URI: str
    REDIS_URL: str
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
