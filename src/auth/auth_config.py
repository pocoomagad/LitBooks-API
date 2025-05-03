from authx import AuthXConfig, AuthX, RequestToken, TokenPayload
import hashlib
from schemas.users import UserLoginSchemaProfPost, UserLoginSchema
from abc import ABC, abstractmethod
from datetime import timedelta
from exceptions.handlers import *

"""Конфиг ауентификации"""

class AbstractConfig(ABC):
    @abstractmethod
    async def logining_in_service():
        raise NotImplementedError
    

    @abstractmethod
    async def create_users():
        raise NotImplementedError


    @abstractmethod
    async def verify_access():
        raise NotImplementedError


class authconfig:
    def __init__(self):
        self.config = AuthXConfig()
        self.security = AuthX(config=self.config)
        self.inciliation = self._inciliation()

    def _inciliation(self):
        self.config.JWT_ALGORITHM = "HS256"
        self.config.JWT_SECRET_KEY = "admin"
        self.config.JWT_ACCESS_COOKIE_NAME = "Authorization_token"
        self.config.JWT_TOKEN_LOCATION = ["cookies"]
        self.config.JWT_ACCESS_CSRF_COOKIE_NAME = "csrf_name"
        self.config.JWT_ACCESS_COOKIE_PATH = "/profile"
        self.config.JWT_COOKIE_CSRF_PROTECT = False
        self.config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=365)
    

    @staticmethod
    async def to_hash(
        password: str
        ):
        hash_pass = hashlib.new("sha256")
        to_hash = password.encode()
        hash_pass.update(to_hash)
        pass_ = hash_pass.hexdigest()
        return pass_
    
    
    async def create_users(
        self, 
        new_user: UserLoginSchemaProfPost
        ): 
        data_user = new_user.model_dump()
        password = await self.to_hash(password=new_user.password)
        data_user["password"] = password
        return data_user
    

    async def logining_in_service(
        self, 
        input_pass: UserLoginSchema,
        creds: str
        ):
        result_creds = list(creds)[1][1]
        author = list(creds)[3][1]
        if await self.to_hash(input_pass.password) == result_creds:
            token = self.security.create_access_token(uid=input_pass.user_name, data={"author": author})
            return token
        raise PasswordException