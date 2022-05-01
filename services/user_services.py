from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_session
from fastapi import Depends
from models.user_models import User, UserCreate


async def select_all_users(session: AsyncSession) -> list[User]:

    result = await session.execute(select(User))
    users = result.scalars().all()
    print(f'{users=}')
    print(f'{type(users)}')
    return users


async def exits_user(new_user: UserCreate, session: AsyncSession) -> bool:

    result = await session.execute(select(User))

    users = result.scalars().all()

    if any(user.username == new_user.username for user in users):
        return True
    else:
        return False


async def get_user(username: str, session: AsyncSession):
    result = await session.execute(select(User).where(User.username == username))

    return result.scalars().first()






