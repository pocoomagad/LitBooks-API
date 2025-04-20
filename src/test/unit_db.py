from web.Depend import SessionDep
from model.books import BookModel



async def add_book(session: SessionDep):
    new_book = BookModel(
        title='12414',
        viewes=3,
        author='dafafda'
    )
    session.add(new_book)
    await session.commit()
    return "Добавлено"

