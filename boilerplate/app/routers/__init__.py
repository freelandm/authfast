from routers.auth import router as auth_router
from routers.static import router as static_router
from routers.health import router as health_router
from routers.users import router as users_router
from routers.items import router as items_router

__all__ = [
    "auth_router",
    "static_router",
    "health_router",
    "users_router",
    "items_router",
]
