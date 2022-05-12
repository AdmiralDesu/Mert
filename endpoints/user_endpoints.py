from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from auth.auth import AuthHandler
from models.user_models import UserCreate, User, UserLogin
from services.user_services import select_all_users, exits_user, get_user
from database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

user_router = APIRouter(tags=['users'])
auth_handler = AuthHandler()


@user_router.post('/registration', status_code=201,
                  description='Registration of new user')
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)) -> JSONResponse:
    exists = await exits_user(user, session=session)
    if exists:
        raise HTTPException(status_code=400, detail='Username already exists')

    hashed_password = auth_handler.get_password_hash(user.password)
    user = User(username=user.username, password=hashed_password)
    print(f'User before refresh {user=}')
    session.add(user)
    await session.commit()
    await session.refresh(user)
    print(f'User after refresh {user=}')
    return JSONResponse(
        status_code=HTTP_201_CREATED,
        content={
            'message': 'Song created',
            'name': user.username
        }
    )


@user_router.post('/login', tags=['users'])
async def login(user: UserLogin, session: AsyncSession = Depends(get_session)):
    user_found = await get_user(username=user.username, session=session)
    if not user_found:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Invalid username and/or password'
        )

    verified = auth_handler.verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Invalid username and/or password'
        )

    token = auth_handler.encode_token(user_found.username)
    return {'token': token}


@user_router.get('/users/me')
async def get_current_user(user: User = Depends(auth_handler.get_current_user)):
    return user.username
