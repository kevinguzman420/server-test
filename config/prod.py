from .default import *

# SQLALCHEMY_DATABASE_URI = f'postgresql://{os.getenv("DEV_DATABASE_USERNAME")}:{os.getenv("DEV_DATABASE_PASSWORD")}@{os.getenv("DEV_DATABASE_HOST")}/{os.getenv("DEV_DATABASE")}?sslmode=require'
SQLALCHEMY_DATABASE_URI = "sqlite:///mydb.db"

APP_ENV = APP_ENV_PRODUCTION