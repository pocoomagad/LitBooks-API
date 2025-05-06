from abc import ABC, abstractmethod
from db.engines import conn
from sqlalchemy import insert, select, update, delete, and_
from sqlalchemy.orm import subqueryload
from model.books import BookModel
from sqlalchemy.exc import IntegrityError, NoResultFound
from model.users import UserLoginModel
from model.cart import CartModel
from exceptions.handlers import *


async def get_book(book_id) -> BookModel:
    async with conn() as session:
        stmt = (
                select(BookModel)
                .filter(BookModel.id==book_id)
                )
        book_obj = await session.execute(stmt)
        await session.commit()
        return book_obj.scalars().first()


async def get_user(user_name) -> UserLoginModel:
        async with conn() as session:
            stmt = (
                select(UserLoginModel)
                .filter(UserLoginModel.user_name==user_name)
                )
            res = await session.execute(stmt)
            await session.commit()
            return res.scalars().first()
        

async def get_cart(user_id, book_id) -> CartModel:
    async with conn() as session:
        stmt = (
            select(CartModel)
            .filter(and_(CartModel.user_id==user_id, CartModel.book_id==book_id))
            )
        cart_obj = await session.execute(stmt)
        await session.commit()
        return cart_obj.scalars().first()
        

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
            raise IsbnUniqueException

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
            raise IsbnUniqueException
        except NoResultFound:
            await session.rollback()
            raise NotFoundException
    
    async def delete_book(self, book_id: int):
        try:
            async with conn() as session:
                book = await get_book(book_id)

                if book is None:
                    raise NotFoundException

                await session.delete(book)
                await session.commit()
        except NoResultFound:
                await session.rollback()
                raise NotFoundException               
                
        
class AbstractAuthRepository(ABC):
    model = UserLoginModel

    @abstractmethod
    async def create_user():
        pass

    @abstractmethod
    async def profile():
        pass

    @abstractmethod
    async def login():
        pass

class AuthRepository(AbstractAuthRepository):
    async def create_user(self, values: dict):
        try:
            async with conn() as session:
                stmt = insert(self.model).values(**values)
                await session.execute(stmt)
                await session.commit()
        except IntegrityError:
            await session.rollback()
            raise AlreadyInUse

    async def login(self, user_name: str):
        async with conn() as session:
            stmt = (
                select(self.model)
                .filter(self.model.user_name==user_name))
            res = await session.execute(stmt)
            try:
                user_creds = res.first()

                if user_creds is None:
                    raise PasswordException
                
                await session.commit()
                return user_creds
            except NoResultFound:
                await session.rollback()
                raise PasswordException


    async def profile(self, user_name: str):
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
    book = BookModel
    model = CartModel

    @abstractmethod
    async def add_to_cart():
        pass

    @abstractmethod
    async def delete_from_cart():
        pass


class CartRepository(AbstractCartRepository):
    async def add_to_cart(self, user_name, book_id):
            async with conn() as session:
                user = await get_user(user_name)

                cart_obj = self.model(
                    book_id=book_id,
                    user_id=user.id
                    )

                session.add(cart_obj)
                try:
                    await session.commit()

                except IntegrityError:
                    await session.rollback()
                    raise CartException


    async def delete_from_cart(self, user_name, book_id):
        async with conn() as session:
            user = await get_user(user_name)
            cart = await get_cart(user.id, book_id)

            if cart is None:
                await session.rollback()
                raise NotFoundException
            
            await session.delete(cart)
            await session.commit()