import datetime
import os
import jwt
from fastapi import Security, HTTPException, Depends
from fastapi.security import\
    HTTPBearer, \
    HTTPAuthorizationCredentials
from passlib.context import CryptContext
from starlette.status import HTTP_401_UNAUTHORIZED
from services.user_services import get_user
from database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

class AuthHandler:
    security = HTTPBearer()
    pad_context = CryptContext(schemes=['bcrypt'])
    secret = os.environ.get('SECRET_KEY')

    def get_password_hash(self, password):
        return self.pad_context.hash(password)

    def verify_password(self, password, hashed_password):
        return self.pad_context.verify(password, hashed_password)

    def encode_token(self, username: str):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8),
            'iat': datetime.datetime.utcnow(),
            'sub': username
        }
        return jwt.encode(payload, self.secret, algorithm='HS256')

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)

    async def get_current_user(self,
                               auth: HTTPAuthorizationCredentials = Security(security),
                               session: AsyncSession = Depends(get_session)):
        credential_exception = HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials'
        )

        username = self.decode_token(auth.credentials)
        if username is None:
            raise credential_exception
        user = await get_user(username=username, session=session)
        if user is None:
            raise credential_exception

        return user








