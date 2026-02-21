from fastapi import FastAPI
from pydantic import BaseModel
from tokenGenerator import gen
from functions import *

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/signup")
def signup_user(username: str, passwd: str, pin: int):
    signRes=signUp(username, passwd)
    return {"result": signRes}

@app.post("/login")
def login_user(username: str, passwd: str):
    loginRes=login(username, passwd)
    if loginRes=="correct!":
        loginT=loginToken(username)
        return {"result": loginRes, "token":loginT}
    else:
        return {"result": loginRes}

@app.post("/loginToken")
def get_login_token(token: str):
    lt=tokenLogin(token)
    return {"user":lt}

@app.post('/userInfo')
def get_User_Info(username: str):
    info=showInv(username)
    return {"info":info}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}