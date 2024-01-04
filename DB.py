import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

passwd=os.getenv('PASSWD')
uri=f'mongodb+srv://dkg:{passwd}@cluster0.zehbxvy.mongodb.net/?retryWrites=true&w=majority'
db = MongoClient(uri)

# print the ip with subnet of machine
print("Your IP address is:")
os.system("curl ifconfig.me")

try:
    db.admin.command('ping')
    print("\nPinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def create(guild_id:int,tname:str,slots:int,team_size:int,role:int): #creates a new guild in the database
    try:
        collection=db[str(guild_id)]
        data=collection["Tournament Config"]
        if tname in data.distinct("Tournament Name"):
            # throw a error
            return "Tournament Name already exists."
        x=data.count_documents({})
        data_inserted_id = data.insert_one({"_id":x+1,"Tournament Name":tname,"slots":slots,"team_size":team_size,"role":role})
        # return the db id
        return data_inserted_id.inserted_id
    except Exception as e:
        print(e)
        return f"Error \n{e}\n\n"
    
def delete(guild_id:int,T_id:int): #deletes a tournament from the config and the tournamnent db
    try:
        collection=db[str(guild_id)]
        data=collection["Tournament Config"]
        data.delete_one({"_id":T_id})
        collection.drop_collection(str(T_id))
    except Exception as e:
        print(e)
        return f"Error \n{e}\n\n"
    
def get(guild_id:int,T_id:int): #returns the tournament config
    try:
        collection=db[str(guild_id)]
        data=collection["Tournament Config"]
        return data.find_one({"_id":T_id})
    except Exception as e:
        print(e)
        return f"Error \n{e}\n\n"