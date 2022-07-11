from fastapi import FastAPI, Query, Path, Body, Cookie
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from enum import Enum

app = FastAPI()


class Name(str, Enum):
    anton = 'anton'
    mike = 'mike'
    john = 'john'


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }


class User(BaseModel):
    username: str
    full_name: str | None = None


class TestItem(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None


class TestImage(BaseModel):
    url: HttpUrl
    name: str


class NestedItem(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[TestImage] | None = None


fake_db = [{'name': 'Mike'}, {'name': 'John'}, {'name': 'Enny'}]


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class NewTestItem(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/test_item_exclude/{item_id}", response_model=NewTestItem, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user


@app.get("/cookie_item/")
async def cookie_item(ads_id: str | None = Cookie(default=None)):
    return ads_id


@app.put("/nested_item/{item_id}")
async def update_nested_item(item_id: int, item: NestedItem):
    results = {"item_id": item_id, "item": item}
    return results


@app.put("/update_items_with_field_pydantic/{item_id}")
async def update_item(item_id: int, item: TestItem = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results


@app.put("/items_body/{item_id}")
async def update_items_body(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: int = Body(gt=0),
    q: str | None = None
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results


@app.put("/put_items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results


"""
 ge - Больше чем или равно
 gt - Больше чем
 le - Меньше чем или равно
 lt - Меньше чем
"""


@app.get("/items/{item_id}")
async def read_items(
    *, item_id: int = Path(title="The ID of the item to get", ge=1), q: str
):

    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.get("/items_path/{item_id}")
async def read_items_with_path(q: str, item_id: int = Path(title="The ID of the item to get")):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.get("/read_items/")
async def read_items(
    q: str
    | None = Query(
        default=None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get('/list_query/')
async def query_list(q: list[str] | None = Query(default=None)):
    q_list = {"q": q}
    return q_list


@app.get('/item_query/')
async def read_item(q: str | None = Query(default=None, max_length=10)):
    res = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        res.update({"q": q})
    return res


@app.put("/new_item_id_with_q/{item_id}")
async def create_item_with_q(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


@app.put("/item_id/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}


@app.put('/price_with_tax/')
async def price_update(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({'price_with_tax': price_with_tax})
    return item_dict


@app.get('/get_item/')
async def create_item(item: Item):
    return item


@app.get("/required_items/{item_id}")
async def read_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@app.get('/items/')
async def get_parameters(skip: int = 0, limit: int = 10):
    return fake_db[skip: limit]


@app.get('/files/{file_path:path}')
async def read_file(file_path: str):
    return {"file_path": file_path}


@app.get('/get_enum_name/{name}')
async def get_enum_name(name: Name):
    if name == Name.anton:
        return {'name': name, 'message': 'You are cool'}
    elif name.value == 'mike':
        return {'name': name, 'message': 'Much better'}
    return {'name': name, 'message': 'Wow, is it you, right?'}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
