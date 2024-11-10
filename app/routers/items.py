from typing import Annotated, Dict
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies.auth import oauth2_scheme
from app.models.items import Item
from app.logger import logger

router = APIRouter(
    prefix="/items",
    tags=["items"],
    # dependencies=[Depends(first_callable_deps), Depends(second_callable_deps), ... ],
    responses={404: {"description": "Not found"}},
)

protected_items_db = {
    "silencer": {"name": "Golden Silencer", "value": 4000},
    "treasure": {"name": "Treasure Chest", "value": 42000},
}

fake_items_db = {
    "plumbus": {"name": "Plumbus", "value": 36},
    "gun": {"name": "Portal Gun", "value": 17},
    "borked": {"name": "Borked Item"},
}

@router.get("/protected")
async def read_protected_items(token: Annotated[str, Depends(oauth2_scheme)]) -> Dict[str, Item]:
    logger.info(f'{token=}')
    return protected_items_db


@router.get("/{item_id}")
async def read_item(item_id: str) -> Item:
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_items_db[item_id]


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}
