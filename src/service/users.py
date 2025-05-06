from repository.repository_db import AbstractAuthRepository
from schemas.users import UserLoginSchema, UserLoginSchemaProfPost, UserLoginSchemaGet
from auth.auth_config import authconfig, AbstractConfig
from authx import TokenPayload

class AuthSerice:
    def __init__(self, user_repo: AbstractAuthRepository, auth_repo: AbstractConfig):
        self.user_repo: AbstractAuthRepository = user_repo()
        self.auth_repo: AbstractConfig = auth_repo()


    @staticmethod
    async def get_name(token: TokenPayload):
        user_name = token.sub
        return user_name


    async def create_users(self, creds: UserLoginSchemaProfPost):
       pass_dict = await self.auth_repo.create_users(new_user=creds.model_dump())
       query = await self.user_repo.create_user(pass_dict)
    

    async def login(self, data: UserLoginSchema):
        query = await self.user_repo.login(data.user_name)
        for row in query:
            pass_ = UserLoginSchemaProfPost.model_validate(row, from_attributes=True)
        response = await self.auth_repo.login(data, pass_)
        return response


    async def get_profile(self, token):
            user_name = await self.get_name(token)
            profile = await self.user_repo.profile(user_name)
            result = [UserLoginSchemaGet.model_validate(row, from_attributes=True) for row in profile]
            return result    