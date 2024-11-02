from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://marko_m:HhfpCcGObwf7Huxn@maincluster.zwq2b.mongodb.net/?retryWrites=true&w=majority&appName=MainCluster"

client = MongoClient(uri, server_api=ServerApi('1'))

database = client["database"]

doc = {
    "Field1": "Testing1",
    "Field2": "Testing2"
}

collection = database["test-write"]

res_write = collection.insert_one(doc)

print(res_write)

