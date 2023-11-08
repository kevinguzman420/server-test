
SECRET_KEY = "9f8f2849f5443d53242d50f96d1f436692795056b8c6f41f6471011dd798e70bba50fb33aefd966a6aff76872da9c313636eb2815ff84cd3cdc44ec5dc3f2044"

# sqlalchemy
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT
JWT_SECRET_KEY = "so-secret"
# to ensure the cookie set in http. Enable in production to https
# JWT_COOKIE_SECURE = False
# JWT_ACCESS_COOKIE_PATH = "/api/"
# JWT_TOKEN_LOCATION = "cookies"
# JWT_COOKIE_CSRF_PROTECT = True # set to get csrf double submit protection.
# JWT_COOKIE_SAMESITE = None
# JWT_ACCESS_COOKIE_NAME = "token_cookie"
# JWT_REFRESH_COOKIE_PATH = "/api/token/refresh"
# JWT_COOKIE_DOMAIN = "localhost"

JWT_TOKEN_LOCATION = ['cookies']
JWT_ACCESS_COOKIE_NAME = 'my-access-token'
JWT_ACCESS_COOKIE_PATH = '/'
JWT_ACCESS_COOKIE_DOMAIN = 'localhost'

# ENVIRONMENTS
APP_ENV_DEVELOPMENT = "DEVELOPMENT"
APP_ENV_PRODUCTION = "PRODUCTION"
APP_ENV_TESTING = "TESTING"

APP_ENV = ""
