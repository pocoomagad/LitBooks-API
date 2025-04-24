from authx import AuthXConfig, AuthX, RequestToken
import hashlib
from schemas.users import UserLoginSchemaProfPost, UserLoginSchema
from fastapi import Response

"""Конфиг ауентификации"""

class authconfig:
    config = AuthXConfig()
    security = AuthX(config=config)

    config.JWT_ALGORITHM = "HS256"
    config.JWT_SECRET_KEY = "admin"
    responce = config.JWT_ACCESS_COOKIE_NAME = "Authorization_token"
    config.JWT_TOKEN_LOCATION = ["cookies"]
    config.JWT_ACCESS_CSRF_COOKIE_NAME = "csrf_name"
    config.JWT_ACCESS_COOKIE_PATH = "/profile"
    
    @staticmethod
    async def to_hash(
        password: str
        ):
        hash_pass = hashlib.new("sha256")
        to_hash = password.encode()
        hash_pass.update(to_hash)
        pass_ = hash_pass.hexdigest()
        return pass_


    @classmethod
    async def logining_in_service(
        cls, 
        input_pass: UserLoginSchema, 
        creds: str
        ):
        if await cls.to_hash(input_pass.password) == creds:
            token = cls.security.create_access_token(uid=input_pass.user_name)
            return token
        
    
    @classmethod
    async def create_users(
        cls, 
        new_user: UserLoginSchemaProfPost
        ): 
        data_user = new_user.model_dump()
        password = await cls.to_hash(password=new_user.password)
        data_user["password"] = password
        return data_user


    @classmethod
    async def verify_access(
        cls, 
        token
        ):
        try:
            result = cls.security.verify_token(token=token)
            return result
        except Exception as e:
            return False