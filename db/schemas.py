from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class FakeItem(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class FakeUser(UserBase):
    id: int
    is_active: bool
    items: list[FakeItem] = []

    class Config:
        orm_mode = True
