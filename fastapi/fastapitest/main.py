from enum import Enum
from typing import List
from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, EmailStr


app = FastAPI()


# First Steps
@app.get("/")
def read_root():
    return {"Hello": "World"}


# Path Parameters
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = 'lenet'


@app.get("/model/{model_name}")
def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"Model_name": model_name, "message": "Deep Learning FTW"}
    if model_name == ModelName.lenet:
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
def read_user_me(file_path: str):
    return {"file_path": file_path}


# Query Parameters
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# @app.get("/items/")
# def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip: skip + limit]


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None, short: bool = True):
#     item = {"item_id": item_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update({"description": "This is an amazing item that has a long description"})
#     return item


@app.get("/users/{user_id}/items/{item_id}")
def read_user_item(user_id: int, item_id: str, q: str = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


#  三种类型的query parameters, 必须，必须有默认值，可选
# @app.get("/items/{item_id}")
# def read_user_item(item_id: str, needy: str, skip: int = 0, limit: int = None):
#     item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
#     return item


# Request Parameters
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
    tags: List[str] = []


# @app.post("/items")
# def create_item(item: Item):
#     item_dict = item.dict()
#     if item.tax:
#         price_with_tax = item.tax + item.price
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict


# @app.put("/items/{item_id}")
# def create_item(item_id: int, item: Item, q: str = None):
#     result = {"item_id": item_id, **item.dict()}
#     if q:
#         result.update({"q": q})
#     return result


# Query Parameters and String Validations
# Query()中...必须，None可选，xxx是必须且有默认值
@app.get("/items/")
def read_items(q: str = Query(..., max_length = 20, min_length = 3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Path Parameters and Numeric Validations
# @app.get("/items/{item_id}")
# def read_items(item_id: int = Path(..., title = "The ID of the item to get"), q: str = Query(None, alias = "item-query")):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     return results


# Body - Multiple Parameters
# @app.put("/items/{item_id}")
# def update_item(
#     *,
#     item_id: int = Path(..., title = "The ID of the item to get", ge = 0, le = 1000),
#     q: str = None,
#     item: Item = None,
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     if item:
#         results.update({"item": item})
#     return results


@app.put("/items/{item_id}")
async def update_item(*, item_id: int, item: Item, importance: int = Body(...), q: str = None):
    results = {"item_id": item_id, "item": item, "importance": importance}
    if q:
        results.update({"q": q})
    return results


# Response Model
@app.post("/items/", response_model=Item)
def create_item(item: Item):
    return item


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str = None


@app.post("/user/", response_model=UserOut)
def create_user(*, user: UserIn):
    return user


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
def read_item(item_id: str):
    return items[item_id]
