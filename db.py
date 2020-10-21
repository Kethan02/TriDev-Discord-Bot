from pymongo import MongoClient
import datetime

user = "discord_user"
pswd = "eUADmtKtHyQU5"
db_name = "data"
collection_name = "messages"
db_link = f"mongodb+srv://{user}:{pswd}@discorddata.cmilw.mongodb.net/{db_name}?retryWrites=true&w=majority"

""" 
This document is a sample of how message docs will look
This specific document is already in the database
"""
messageDocument = {
  "user": "Alan",
  "content": "Anyone want to go surfing friday?",
  "timestamp": datetime.datetime(1954, 6, 7, 11, 40)
}

def connectToDB(link):
    client = MongoClient(link)
    return client[db_name]


def main():
    db = connectToDB(db_link)
    collection = db[collection_name]
    print(collection.find_one({ "user": "Alan" }))

main()
