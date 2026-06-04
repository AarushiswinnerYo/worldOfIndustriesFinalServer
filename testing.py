from pymongo import MongoClient

client=MongoClient("mongodb+srv://W:a@woiserver.38gfy.mongodb.net/")
db=client.Users

print(db.prices.find_one({"buyprices":{"$exists":True}}, {'_id':0})["buyprices"]["steel"])