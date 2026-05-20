from fastapi import FastAPI
from pydantic import BaseModel
from tokenGenerator import gen
from functions import *
from fastapi.staticfiles import StaticFiles

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.mount("/.well-known", StaticFiles(directory=".well-known"), name="well-known")

@app.post("/signup")
def signup_user(username: str, passwd: str):
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

@app.post("/buyPrices")
def get_buy_prices():
    prices=getBuyPrices()
    return prices["buyprices"]

@app.post("/buy")
def buy_materials(token: str, amount: int, passwd: str, ):
    return

@app.post("/sellPrices")
def get_sell_prices():
    pricesSell=getSellPrices()
    return pricesSell["sellprices"]

@app.post('/userInfo')
def get_User_Info(token: str):
    info=showInv(token)
    return {"info":info}