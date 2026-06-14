from fastapi import FastAPI
from pydantic import BaseModel
from tokenGenerator import gen
from functions import *
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

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

@app.post("/craftPrices")
def get_craft_prices():
    pricesCraft=getCraftPrices()
    return pricesCraft["craftingPrices"]["recipes"]

@app.post("/buy")
def buy_materials(token: str, amount: int, passwd: str, material_name:str, material_subtype=""):
    return buyFunc(token=token, amount=amount, passwd=passwd, materialName=material_name,materialSubType=material_subtype)

@app.post("/sell")
def sell_materials(token: str, amount: int, passwd: str, material_name:str, material_subtype=""):
    return sellFunc(token=token, amount=amount, passwd=passwd, materialName=material_name,materialSubType=material_subtype)

@app.post("/sellrec")
def sell_recipe(token: str, amount: int, passwd: str, material_name:str, material_subtype=""):
    return sellRecipeFunc(token=token, amount=amount, passwd=passwd, materialName=material_name,materialSubType=material_subtype)

@app.post("/sellRecipePrices")
def get_recipe_selling_prices():
    pricesSellRecipe=getRecipeSellPrices()
    return pricesSellRecipe["sellRecipe"]["recipes"]

@app.post("/craft")
def craft_recipes(token: str, amount: int, passwd: str, recipe_name:str, recipe_subtype=""):
    return craftRecipeFunc(token=token, amount=amount, passwd=passwd, materialName=recipe_name,materialSubType=recipe_subtype)

@app.post("/sellPrices")
def get_sell_prices():
    pricesSell=getSellPrices()
    return pricesSell["sellprices"]

@app.get("/likes{song_id}")
def get_likes(song_id: int):
    return getLikes(song_id)

@app.post("/like{song_id}")
def like_song(song_id: int):
    print(f"Received raw payload: {song_id}")
    return like(song_id)

@app.post("/unlike{song_id}")
def unlike_song(song_id: int):
    return unlike(song_id)

@app.post('/userInfo')
def get_User_Info(token: str):
    info=showInv(token)
    return {"info":info}