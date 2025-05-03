from repository.repository_db import AbstractCartRepository

class CartService:
    def __init__(self, cart_repo: AbstractCartRepository):
        self.cart_repo: AbstractCartRepository = cart_repo()

    @staticmethod
    async def get_name_cart(token):
        user_name = dict(token).get("sub")
        return user_name
    

    async def add_to_cart(self, book_id, token):
        name = await self.get_name_cart(token)
        query = await self.cart_repo.add_to_cart(name, book_id)
    

    async def delete_from_cart(self, book_id, token):
        name = await self.get_name_cart(token)
        query = await self.cart_repo.delete_from_cart(name, book_id)