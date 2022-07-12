from fastapi import FastAPI, APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

fake_db = {}


class SecondItem(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@router.get("/api_s/sec_items/{item_id}", response_model=SecondItem)
async def read_item(item_id: str):
    return items[item_id]


@router.patch("/api_s/sec_items/{item_id}", response_model=SecondItem)
async def update_item(item_id: str, item: SecondItem):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item


class FakeItem(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None


@router.put("/api_s/items/{id}")
def update_item(id: str, item: FakeItem):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
    return fake_db


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


@router.post("/api_s/items_post/", response_model=Item, tags=["items"])
async def create_item(item: Item):
    """
        Create an item with all the information:

        - **name**: each item must have a name
        - **description**: a long description
        - **price**: required
        - **tax**: if the item doesn't have tax, you can omit this
        - **tags**: a set of unique tag strings for this item
        """
    return item


@router.get("/api_s/items_get/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@router.get("/api_s/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]
