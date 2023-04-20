from typing import Optional

from app.api import deps
from app.core import user_manager, recognize
from app.models import ItemTable, UserTable
from app.schemas.requests import ItemCreateRequest, ItemUpdateRequest
from app.schemas.responses import ItemResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.recognize import AudioProcessing

ap = AudioProcessing()

router = APIRouter()

@router.get("/me", response_model=list[ItemResponse], status_code=200)
async def get_all_my_items(
    session: AsyncSession = Depends(deps.get_async_session),
    current_user: UserTable = Depends(user_manager.get_current_user),
):
    """Get list of items for currently logged user."""

    items = await session.execute(
        select(ItemTable)
        .where(
            ItemTable.user_id == current_user.id,
        )
        .order_by(ItemTable.text)
    )
    return items.scalars().all()


@router.get("/{id}", response_model=ItemResponse, status_code=200)
async def get_item(
    id: int,
    session: AsyncSession = Depends(deps.get_async_session),
    current_user: UserTable = Depends(user_manager.get_current_user),
):
    """Get item by id."""
    # item = await session.execute(
    #     select(ItemTable)
    #     .where(ItemTable.id == id)
    #     .where(ItemTable.user_id == current_user.id)
    # )
    # if item is None:
    #     raise HTTPException(status_code=404, detail="Item not found")
    # if item.user_id != current_user.id:
    #     raise HTTPException(status_code=403, detail="Not allowed")
    # print(item.scalars().all())
    # return item.scalars().all()
    item: Optional[ItemTable] = await session.get(ItemTable, id)
    if not item or item.user_id != current_user.id:
        raise HTTPException(404)
    return item


@router.post("/create", response_model=ItemResponse, status_code=201)
async def create_new_item(
    new_item: ItemCreateRequest = Depends(),
    session: AsyncSession = Depends(deps.get_async_session),
    current_user: UserTable = Depends(user_manager.get_current_user),
):
    """Creates new item. Only for logged users."""
    item = ItemTable(user_id=current_user.id, text=ap.recognition(new_item.text))

    session.add(item)
    await session.commit()
    return item


@router.patch("/{id}", response_model=ItemResponse)
async def update_item(
    id: int,
    item_in: ItemUpdateRequest,
    session: AsyncSession = Depends(deps.get_async_session),
    current_user: UserTable = Depends(user_manager.get_current_user),
):
    item: Optional[ItemTable] = await session.get(ItemTable, id)
    if not item or item.user_id != current_user.id:
        raise HTTPException(404)
    update_data = item_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    session.add(item)
    await session.commit()
    return item

@router.delete("/{id}", status_code=204)
async def delete_item(
    id: int,
    session: AsyncSession = Depends(deps.get_async_session),
    current_user: UserTable = Depends(user_manager.get_current_user),
):
    item: Optional[ItemTable] = await session.get(ItemTable, id)
    if not item or item.user_id != current_user.id:
        raise HTTPException(404)
    await session.delete(item)
    await session.commit()
    return None