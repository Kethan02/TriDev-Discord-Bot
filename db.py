from pymongo import MongoClient
import datetime

user = "discord_user"
pswd = "eUADmtKtHyQU5"
db_name = "messages"
guild_name = "Test Server"
db_link = f"mongodb+srv://{user}:{pswd}@discorddata.cmilw.mongodb.net/{db_name}?retryWrites=true&w=majority"

""" 
This document is a sample of how message docs will look
This specific document is already in the database
"""
messageDocumentSchema = {
  "user": "Charles",
  "content": "Hello, there sir",
  "timestamp": datetime.datetime(1954, 6, 7, 11, 40)
}

def connect_to_db(link, db_name):
  """Returns the database of all stored messages."""
  client = MongoClient(link)
  db = client[db_name]
  print("Connected successfully to database!")
  return db

def get_collection(db_object, collection_name):
  """
  Returns the collection of messages of a specific guild.

  The way messages are stored, each guild has its own a collection containing
  all of that guild's message documents.
  """
  return db_object[collection_name]

def get_messages(collection_object, user_name):
  """
  Returns the messages of a specific guild, with the exception of messages
  authored by the given user.
  """
  return collection_object.find({ "user": { "$ne": user_name } })
#We need to have the add message return its time stamp apparently because Kethan wants to use its time stamp to
#decide if he wants to retrieve the message or not.
def add_message(collection_object, user_name, message, timestamp):
  """
  Adds a message document to the database.
  Returns the id of the document if the transaction was successful.
  """
  document = {
    "user": user_name,
    "content": message,
    "timestamp": timestamp
  }
  x = collection_object.insert_one(document)
  return x.inserted_id
  # I thought we needed a function that adds keywords to the database
def add_keyword(collection_keywords,user_name, keyword, timestamp):
    "Adds a keyword document to the database"
    "Returns the timestamp of the dobument if the transaction was successful."
    document = {
      "user":user_name,
      "content":keyword,
      "timestamp":timestamp
    }
    x = collection_keywords.insert_one(document)
    return x.inserted_timestamp


def main():
  # Connects to database and gets collection
  db = connect_to_db(db_link, db_name)
  collection = get_collection(db, guild_name)

  # Gets and prints out the messages in the collection
  messages = get_messages(collection, "Holden")
  for m in messages:
    print(m)

main()
