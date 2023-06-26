from pydantic import BaseSettings, MongoDsn


class AppSettings(BaseSettings):
    mongo_connection_string: MongoDsn
    appinsights_connection_string: str = None

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = AppSettings()
