import os
import pandas as pd
from binance import Client
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

pd.set_option('display.float_format', '{:.10f}'.format)
pd.set_option('display.max_columns', 50)

load_dotenv()


class Settings(BaseSettings):
    API_KEY: str = os.environ.get("API_KEY")
    API_SECRET: str = os.environ.get("API_SECRET")

    class Config:
        env_file = "algo-trading/.env"
        env_file_encoding = "utf-8"


config = Settings()
