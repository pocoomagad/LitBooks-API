from dotenv import load_dotenv
import os
from os.path import join, dirname

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT= os.getenv('DB_PORT')
DB_USER= os.getenv('DB_USER')
DB_PASS= os.getenv('DB_PASS')
DB_NAME= os.getenv('DB_NAME')


DATABASE_URL_asyncpg = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@127.0.0.1:{DB_PORT}/{DB_NAME}"




