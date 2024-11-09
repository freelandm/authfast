from fastapi import FastAPI
from routers import static_router, health_router, items_router, users_router, auth_router

# add global dependency checks, applied to all routes
#app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()

app.include_router(auth_router)
app.include_router(static_router)
app.include_router(health_router)
app.include_router(users_router)
app.include_router(items_router)
#app.include_router(
#    admin.router,
#    prefix="/admin",
#    tags=["admin"],
#    dependencies=[Depends(get_token_header)],
#    responses={418: {"description": "I'm a teapot"}},
#)

