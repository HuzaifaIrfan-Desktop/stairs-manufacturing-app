from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    company_name: str = "Treads By Design"
    __version__: str = "0.1.2"

    developer_name: str = "Huzaifa Irfan"
    developer_email: str = "hi@huzaifairfan.com"
    developer_url: str = "https://huzaifairfan.com"

settings = Settings()