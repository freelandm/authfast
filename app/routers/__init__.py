from app.routers.auth import router as auth_router
from app.routers.static import router as static_router
from app.routers.health import router as health_router
from app.routers.users import router as users_router
from app.routers.items import router as items_router
from app.routers.email import router as email_router

__all__ = [
    "auth_router",
    "static_router",
    "health_router",
    "users_router",
    "items_router",
    'email_router',
]
