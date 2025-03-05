from typing import Union

from fastapi import FastAPI, status, UploadFile, File, Security, Depends
from pydantic import BaseModel

from typing import Annotated


## from .db import User
## from .security import get_current_active_user

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.get("/tests/", status_code=status.HTTP_418_IM_A_TEAPOT)
def read_items():
    return [{"name": "Plumbus"}, {"name": "Portal Gun"}]    

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


@app.get("/items2/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items3/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

##@app.get("/users/me/items/")
##async def read_own_items(
#3    current_user: Annotated[User, Security(get_current_active_user, scopes=["items"])]
##):
##    return [{"item_id": "Foo", "owner": current_user.username}]

