from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routers import static_router, health_router, items_router, users_router, auth_router, email_router
from app.logger import logger

from app.scripts import bootstrap


# add global dependency checks, applied to all routes
#app = FastAPI(dependencies=[Depends(get_query_token)])
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run migrations
    #alembic_cfg = Config("alembic.ini")
    #command.upgrade(alembic_cfg, "head")

    #SQLModel.metadata.create_all(engine)
    bootstrap()
    yield

app = FastAPI(lifespan=lifespan)

@app.exception_handler(Exception)
async def handle_exception(req: Request, e: Exception):
    return JSONResponse(
        status_code=500,
        content=f"Application error: {e}"
    )

app.include_router(auth_router)
app.include_router(static_router)
app.include_router(health_router)
app.include_router(users_router)
app.include_router(items_router)
app.include_router(email_router)

#app.include_router(
#    admin.router,
#    prefix="/admin",
#    tags=["admin"],
#    dependencies=[Depends(get_token_header)],
#    responses={418: {"description": "I'm a teapot"}},
#)

