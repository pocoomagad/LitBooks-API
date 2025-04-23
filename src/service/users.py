from repository.repository_db import AbstractAuthRepository
from schemas.users import UserLoginSchema, UserLoginSchemaProfPost
from auth.auth_config import AuthConfig_

class AuthSerice:
    def __init__(self, user_repo: AbstractAuthRepository):
        self.user_repo: AbstractAuthRepository = user_repo()

    async def create_users(self, creds: UserLoginSchemaProfPost):
       pass_dict = await AuthConfig_.create_users(new_user=creds)
       query = await self.user_repo.create_user(pass_dict)
       return query
    

    async def auths_in(self, data: UserLoginSchema):
        login_dict = data.model_dump()
        query = await self.user_repo.auth_in(login_dict.get("user_name"))
        responce = await AuthConfig_.logining_in_service(data, query)
        return responce


    async def protecteds():
        pass