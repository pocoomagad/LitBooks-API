from repository.repository_db import AbstractAuthRepository
from schemas.users import UserLoginSchema, UserLoginSchemaProfPost
from auth.auth_config import authconfig

class AuthSerice:
    def __init__(self, user_repo: AbstractAuthRepository):
        self.user_repo: AbstractAuthRepository = user_repo()

    async def create_users(self, creds: UserLoginSchemaProfPost):
       pass_dict = await authconfig.create_users(new_user=creds)
       query = await self.user_repo.create_user(pass_dict)
       return query
    

    async def auths_in(self, data: UserLoginSchema):
        login_dict = data.model_dump()
        query = await self.user_repo.auth_in(login_dict.get("user_name"))
        responce = await authconfig.logining_in_service(data, query)
        return responce


    async def protecteds(self, token):
        login_token = await authconfig.verify_access(token=token)
        return login_token