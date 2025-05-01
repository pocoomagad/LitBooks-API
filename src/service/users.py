from repository.repository_db import AbstractAuthRepository
from schemas.users import UserLoginSchema, UserLoginSchemaProfPost, UserLoginSchemaGet
from auth.auth_config import authconfig, AbstractConfig

class AuthSerice:
    def __init__(self, user_repo: AbstractAuthRepository, auth_repo: AbstractConfig):
        self.user_repo: AbstractAuthRepository = user_repo()
        self.auth_repo: AbstractConfig = auth_repo()


    @staticmethod
    async def get_name(token):
        user_name = dict(token).get("sub")
        return user_name


    async def create_users(self, creds: UserLoginSchemaProfPost):
       pass_dict = await self.auth_repo.create_users(new_user=creds)
       query = await self.user_repo.create_user(pass_dict)
       return query
    

    async def auths_in(self, data: UserLoginSchema):
        login_dict = data.model_dump()
        query = await self.user_repo.auth_in(login_dict.get("user_name"))
        if not query:
            return False
        result_creds = [UserLoginSchemaProfPost.model_validate(row, from_attributes=True) for row in query]
        response = await self.auth_repo.logining_in_service(data, result_creds[0])
        return response


    async def protecteds(self, token):
            user_name = await self.get_name(token)
            profile = await self.user_repo.protected(user_name)
            result = [UserLoginSchemaGet.model_validate(row, from_attributes=True) for row in profile]
            return result    