from pymongo import MongoClient
import datetime

user = "discord_user"
pswd = "eUADmtKtHyQU5"
db_names = ["keywords", "messages"]
guild_name = "Test Server"
collection_keywords_name = "keywords"

""" 
This document is a sample of how message docs will look.
The keyword field is for the keyword that caused the message to be flagged.
The timestamp field is the time the message was sent, and will be used to
periodically clear out the database.
"""
messageDocumentSchema = {
  "user": "Charles",
  "keyword": "sir",
  "content": "Hello, there sir",
  "timestamp": datetime.datetime(1954, 6, 7, 11, 40)
}

""" 
This document is a sample of how keyword docs will look.
The keywords are what the on_message will actually search for, the category is
just a clever way to organize words to make slang detection easier.
"""
keywordDocumentSchema = {
  "category": "Homework",
  "keywords": ["hw", "homework"]
}

def connect_to_db(user, pswd, db_name):
  """Returns a database object."""
  link = f"mongodb+srv://{user}:{pswd}@discorddata.cmilw.mongodb.net/{db_name}?retryWrites=true&w=majority"
  client = MongoClient(link)
  db = client[db_name]
  print("Connected successfully to database!")
  return db

def get_collection(db_object, collection_name):
  """Returns a collection contained in a database."""
  return db_object[collection_name]

def get_messages(collection_object, user_name):
  """
  Returns the messages of a specific guild (collection), with the exception of
  messages authored by the given user.
  """
  return collection_object.find({ "user": { "$ne": user_name } })

def add_message(collection_object, user_name, message, timestamp):
  """
  Adds a message document to the database.
  Returns the timestamp of the document if the transaction was successful.
  """
  document = {
    "user": user_name,
    "content": message,
    "timestamp": timestamp
  }
  x = collection_object.insert_one(document)
  return x.inserted_id.generation_time

def add_keyword(collection_keywords, keyword_category, keywords):
  """
  Adds a keyword document to the database.

  keyword_category -- refers to the general idea (i.e. "Homework").

  keywords -- is the list (must be a list even with a single keyword) of words you
  are actually searching for (i.e. "hw" and "homework").

  Returns the timestamp of the document if the transaction was successful.
  """
  document = {
    "category": keyword_category,
    "keywords": keywords
  }
  x = collection_keywords.insert_one(document)
  return x.inserted_id.generation_time

def get_keywords(collection_keywords):
  """
  Returns the list of all keywords to search for.
  """
  cursor = collection_keywords.find({})
  keywords = []
  for document in cursor:
    for word in document["keywords"]:
      keywords.append(word)
  return keywords


def main():
  # Connects to database and gets collection
  db = connect_to_db(user, pswd, db_names[0])
  collection = get_collection(db, "keywords")

  # Gets and prints out the messages in the collection
  keywords = get_keywords(collection)
  for w in keywords:
    print(w)

# This is just some code for testing. If you want to test anything,
# just uncomment main()
# main()
