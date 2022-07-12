from typing import Union, List, Dict


from fastapi import APIRouter, Form, File, UploadFile, Request
from pydantic import BaseModel, EmailStr

router = APIRouter()


@router.post("/api/with_form/")
async def create_with_form(
    file: bytes = File(), fileb: UploadFile = File(), token: str = Form()
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }


@router.post("/api/list_files/")
async def create_multi_files(
    files: list[bytes] = File(description="Multiple files as bytes"),
):
    return {"file_sizes": sum([len(file) for file in files])}


@router.post('/api/files/')
async def create_single_file(file: bytes | None = File(default=None)):
    if not file:
        return {"message": "No such file"}
    else:
        return {"file_size": len(file)}


@router.post("/api/upload_file/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


@router.post("/api/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}


@router.get("/api/keyword-weights/", response_model=Dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}


class Item(BaseModel):
    name: str
    description: str


get_items = [
    {"name": "John", "description": "Strong"},
    {"name": "Mike", "description": "Weak"}
]


@router.get('/api/get_item/', response_model=List[Item])
async def read_item():
    return get_items


class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"


class PlaneItem(BaseItem):
    type = "plane"
    size: int


items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


@router.get("/api/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@router.post("/api/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved
