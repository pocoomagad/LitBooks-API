from abc import ABC, abstractmethod
from db.engines import conn
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import subqueryload
from model.books import BookModel
from sqlalchemy.exc import IntegrityError, NoResultFound
from model.users import UserLoginModel
from model.cart import CartModel

class Abstract_Repository(ABC):
    model = BookModel

    @abstractmethod
    async def add_book():
        raise NotImplementedError

    @abstractmethod     
    async def return_book():
        raise NotImplementedError
       
    @abstractmethod
    async def patch_book():
        raise NotImplementedError
       
    @abstractmethod
    async def delete_book():
        raise NotImplementedError
       

class BookRepository(Abstract_Repository):
    async def add_book(self, data: dict):
        try:
            async with conn() as session:
                    stmt = insert(self.model).values(**data)
                    res = await session.execute(stmt)
                    await session.commit()
        except IntegrityError:
            await session.rollback()
            return "Error : isbn must be unique"

    async def return_book(self, limit: int, offset: int):
        async with conn() as session:
            stmt = select(self.model).limit(limit).offset(offset)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalars().all()

    async def patch_book(self, book_id: int, update_data: dict):
        try:
            async with conn() as session:
                stmt = update(self.model).values(**update_data).filter(self.model.id==book_id).returning(self.model.id)
                res = await session.execute(stmt)
                await session.commit()
                return res.scalar_one()
        except IntegrityError:
            await session.rollback()
            return "Error : isbn must be unique"
        except NoResultFound:
            await session.rollback()
            return False
    
    async def delete_book(self, book_id: int):
        try:
            async with conn() as session:
                stmt = delete(self.model).filter_by(id=book_id).returning(self.model.id)
                res = await session.execute(stmt)
                await session.commit()
                return res.scalar_one()
        except NoResultFound:
                await session.rollback()
                return False                
                
        
class AbstractAuthRepository(ABC):
    model = UserLoginModel

    @abstractmethod
    async def create_user():
        pass

    @abstractmethod
    async def protected():
        pass

    @abstractmethod
    async def auth_in():
        pass

class AuthRepository(AbstractAuthRepository):
    async def _get_by_user_name(self, user_name):
        async with conn() as session:
            stmt = (
                select(self.model.id)
                .filter(self.model.user_name==user_name))
            await session.execute(stmt)
            await session.commit()
        

    async def create_user(self, values: dict):
        try:
            async with conn() as session:
                stmt = insert(self.model).values(**values)
                await session.execute(stmt)
                await session.commit()
        except IntegrityError:
            await session.rollback()
            return "Error : name or password already use"


    async def auth_in(self, user_name: str):
        async with conn() as session:
            try:
                stmt = (
                    select(self.model)
                    .filter(self.model.user_name==user_name))
                res = await session.execute(stmt)
                await session.commit()
                return res.scalars().all()
            except NoResultFound:
                await session.rollback()
                return False


    async def protected(self, user_name: str):
        async with conn() as session:
            stmt = (
                select(self.model)
                .filter(self.model.user_name==user_name)
                .options(subqueryload(self.model.cart))
                    )
            res = await session.execute(stmt)
            await session.commit()
            return res.scalars().all()
        

class AbstractCartRepository:
    user = UserLoginModel
    model = CartModel

    @abstractmethod
    async def add_to_cart():
        pass


class CartRepository(AbstractCartRepository):

        @classmethod
        async def _get_by_user_name(cls, user_name):
            async with conn() as session:
                stmt = (
                    select(cls.user.id)
                    .filter(cls.user.user_name==user_name))
                res = await session.execute(stmt)
                await session.commit()
                return res.scalar_one_or_none()

        async def add_to_cart(self, book_id, user_name):
            async with conn() as session:
                user_id = await self._get_by_user_name(user_name)
                book = CartModel(
                    book_id=book_id,
                    user_id=user_id
                    )
                session.add(book)
                await session.commit()