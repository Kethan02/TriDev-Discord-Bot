from pymongo import MongoClient
import datetime

"""Credentials are needed to log into the database"""
user = "discord_user"
pswd = "eUADmtKtHyQU5"

"""
The databse name is the same as the guild name
(except spaces are replaced with underscores)
"""
db_name = "Test_Server"

"""user_data will be used in the future once we add more features"""
collections = ["keywords", "user_data", "messages"]

""" 
This document is a sample of how message docs will look.
The keyword field is for the keyword that caused the message to be flagged.
The timestamp field is the time the message was sent, and will be used to
periodically clear out the database.
"""
message_document_schema = {
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
keyword_document_schema = {
  "category": "Homework",
  "keywords": ["hw", "homework", "HW", "Homework"]
}

def connect_to_db(user, pswd, db_name):
  """Returns a database object which is used to get data for each guild"""
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
  # Connects to database and gets collection (slow)
  test_server_db = connect_to_db(user, pswd, db_name)
  # Gets a collection of data (fast)
  keywords_collection = get_collection(test_server_db, "keywords")
  # Gets and prints out the messages in the collection (very fast)
  keywords = get_keywords(keywords_collection)
  for w in keywords:
    print(w)

"""
This is just some code for testing.
If you want to test anything, just uncomment main()
"""

main()
