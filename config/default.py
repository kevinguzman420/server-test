from datetime import timedelta

SECRET_KEY = "9f8f2849f5443d53242d50f96d1f436692795056b8c6f41f6471011dd798e70bba50fb33aefd966a6aff76872da9c313636eb2815ff84cd3cdc44ec5dc3f2044"

# sqlalchemy
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT
JWT_SECRET_KEY = "so-secret"
# to ensure the cookie set in http. Enable in production to https
JWT_COOKIE_SECURE = True
JWT_COOKIE_SAMESITE = "Lax"
JWT_TOKEN_LOCATION = ['headers']
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

SESSION_COOKIE_HTTPONLY = False

# BASE URLS
DEV_BASE_URL = "http://localhost:5173"
PROD_BASE_URL = "https://domainname.com"

BASE_URL = ""

# ENVIRONMENTS
APP_ENV_DEVELOPMENT = "DEVELOPMENT"
APP_ENV_PRODUCTION = "PRODUCTION"
APP_ENV_TESTING = "TESTING"

APP_ENV = ""
