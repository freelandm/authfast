from typing import Annotated
from fastapi import Depends, FastAPI
from dependencies import get_query_token
from fastapi.security import OAuth2PasswordBearer
from routers import static_router, health_router, items_router, users_router

app = FastAPI(dependencies=[Depends(get_query_token)])


app.include_router(static_router)
app.include_router(health_router)
app.include_router(users_router)
app.include_router(items_router)
# app.include_router(
#    admin.router,
#    prefix="/admin",
#    tags=["admin"],
#    dependencies=[Depends(get_token_header)],
#    responses={418: {"description": "I'm a teapot"}},
# )


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
