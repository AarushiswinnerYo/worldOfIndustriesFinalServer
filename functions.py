import os
import ast
import pickle
from pymongo import MongoClient
import tokenGenerator as tg

cluster=os.getenv("MDB_CLUST")
client=MongoClient(cluster)
db=client.Users
profs=db.names
tl=db.loginTokens
lists=db.listings
price=db.prices
resources=["wood", "steel", "plants", "metal", "plastic"]
materials={"steel":["type1","type2","type3"], "plants":["cotton","wool","silk","bamboo","tomato","onion"],"metal":["iron", "tungsten","copper"], "wood":["wood"],"plastic":["plastic"]}
def signUp(user, passwd):
    j=profs.find_one({f"{user}": {'$exists': True}})
    if j==None:
        c={"_id":f"{user}",f"{user}":passwd,
           "wood":50,
           "steel":{"type1":0, "type2":0, "type3":0},
           "plants":{"cotton":0, "wool":0, "silk":0, "bamboo":0, "tomato":0, "onion":0},
           "metal":{"iron":0, "tungsten":0, "copper":0},
           "plastic":0,
           "money":10000,
           "group":"None"}
        profs.insert_one(c)
        return "Done!"
    else:
        return "User exists!"

def listListings(typeOfMaterial,material):
    material.lower()
    allLists=lists.find_one({"_id":"lists"})
    finalList=allLists[material][typeOfMaterial]
    print(finalList)
    return finalList

def buyFunc(token, amount, passwd, materialName, materialSubType=""):
    userNameData=tl.find_one({"token": token})
    username=userNameData['_id']
    material_price=price.find_one({"buyprices":{"$exists":True}}, {'_id':0})["buyprices"][materialName]
    if materialSubType=="":
        query={"_id":username}
        userData=profs.find_one(query)
        total=material_price*amount
        if userData[username]==passwd:
            if userData["money"]>=total:
                update_operation={"$set":{"money": userData["money"]-total, materialName:userData[materialName]+amount}}
                profs.update_one(query, update_operation)
                return {"result":"Success"}
            else:
                return {"result":"Not Sufficient Funds"}
        else:
            return {"result":"Incorrect Password"}
    else:
        query={"_id":username}
        userData=profs.find_one(query)
        total=material_price[materialSubType]*amount
        if userData[username]==passwd:
            if userData["money"]>=total:
                update_operation={"$set":{"money": userData["money"]-total, materialName{materialSubType]:userData[materialName][materialSubType]+amount}}}
                profs.update_one(query, update_operation)
                return {"result":"Success"}
            else:
                return {"result":"Not Sufficient Funds"}
        else:
            return {"result":"Incorrect Password"}

def getBuyPrices():
    prices=price.find_one({"buyprices":{'$exists': True}}, {"_id":0})
    return prices

def getSellPrices():
    pricesSell=price.find_one({"sellprices":{"$exists": True}}, {"_id":0})
    return pricesSell

def showInv(token):
    f=tl.find_one({"token":token})
    user=f["_id"]
    if profs.find_one({user: {'$exists': True}})!=None:
        l=profs.find_one({"_id":user},{"_id":0, user:0})
        return l

def passChange(user,oldPasswd,newPasswd):
    r=profs.find_one({user: {'$exists': True}})
    if r!=None:
        if profs.find_one({user:oldPasswd}):
            profs.update_one({user:oldPasswd},{"$set":{user: newPasswd}})
            return "password changed"
        else:
            return "wrong current password"
    else:
        return "no user"

def loginToken(user):
    token=tg.gen(50)
    if tl.find_one({"_id":user})!=None:
        tl.update_one({"_id":user},{"$set":{"token":token}})
    else:
        tl.insert_one({"_id":user, "token":token})
    return token


def tokenLogin(token):
    f=tl.find_one({"token":token})
    if f==None:
        return "Token not found!"
    else:
        return f["_id"]

def login(user, passwd):
    f=profs.find_one({user: {'$exists': True}})
    if f==None:
        return "User not found!"
    else:
        if profs.distinct(user)==[passwd]:
            print(profs.distinct(user))
            print(type(profs.distinct(user)))
            return "correct!"
        else:
            return "incorrect!"
