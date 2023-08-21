from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy
from fastapi import APIRouter, Depends, Form, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import models
from fastapi_users.authentication import Authenticator
from fastapi_users.db import BaseUserDatabase
from fastapi_users.router.common import ErrorCode
from auth.manager import get_user_manager
from auth.models import User
from config import Settings


cookie_transport = CookieTransport(cookie_name="bonds", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=Settings.SECRET_AUTH, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

# user_manager = get_user_manager()

# def get_auth_router(
#     backend: auth_backend,
#     user_db: BaseUserDatabase[user_manager],
#     authenticator: Authenticator,
# ) -> APIRouter:
#     router = APIRouter()

#     @router.post("/login")
#     async def login(
#         response: Response, email: str = Form(), password: str = Form()
#     ):
#         credentials = OAuth2PasswordRequestForm(username=email, password=password)
#         user = await user_db.authenticate(credentials)

#         if user is None or not user.is_active:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
#             )

#         return await backend.get_login_response(user, response)

#     if backend.logout:
#         @router.post("/logout")
#         async def logout(
#             response: Response, user=Depends(authenticator.get_current_active_user)
#         ):
#             return await backend.get_logout_response(user, response)

#     return router


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


current_user = fastapi_users.current_user()