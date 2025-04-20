from authx import AuthXConfig, AuthX
import hashlib

"""Конфиг авторизации"""

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)

token = security.create_access_token()