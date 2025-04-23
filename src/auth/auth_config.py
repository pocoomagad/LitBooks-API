from authx import AuthXConfig, AuthX, RequestToken
import hashlib
from schemas.users import UserLoginSchemaProfPost, UserLoginSchema
from fastapi import HTTPException, Depends

"""Конфиг авторизации"""

class AuthConfig_:
    config = AuthXConfig(
    JWT_ALGORITHM = "HS256",
    JWT_SECRET_KEY = "admin",
    JWT_TOKEN_LOCATION = ["headers"],
    )

    security = AuthX(config=config)

    @staticmethod
    async def to_hash(
        self,
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
        input_pass: UserLoginSchema, creds: str
        ):
        if await cls.to_hash(input_pass.password) == creds:
            token = cls.security.create_access_token(uid=input_pass.user_name)
            return {"access_token": token}
        
    
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
    async def verify_access(cls, token: RequestToken = Depends()):
        try:
            cls.security.verify_token(token=token)
        except Exception as e:
            return False