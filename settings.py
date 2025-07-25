from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    company_name: str = "Treads By Design"
    __version__: str = "0.1.0"

settings = Settings()