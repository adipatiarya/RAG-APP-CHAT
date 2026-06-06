from fastapi import APIRouter
from .routes import role
from .routes import auth
from .routes import user
from .routes import features
from .routes import faq

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(features.router)
api_router.include_router(role.router)
api_router.include_router(user.router)
api_router.include_router(faq.router)