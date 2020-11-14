"""
This module contains everything needed to interface with the mongodb database.
"""

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

def connect_to_mongo(user, pswd):
  """
  Returns a client object that can be used to access all data.

  NOTE: This function is slow. Authenticating takes a few seconds at least.
  """
  link = f"mongodb+srv://{user}:{pswd}@discorddata.cmilw.mongodb.net"
  client = MongoClient(link)
  print("Connected successfully to mongodb!")
  return client

def get_db(client_obj, db_name):
  """
  Returns a database object which is used to get data for each guild

  db_name -- is the name of the desired guild with _'s instead of spaces
  """
  return client_obj[db_name]

def get_collection(db_obj, collection_name):
  """Returns a collection contained in a database."""
  return db_obj[collection_name]

def get_messages(collection_obj, user_name):
  """
  Returns the messages flagged by the keywords, with the exception of
  messages authored by the given user.

  This method should be used when creating the newsletter
  """
  return collection_obj.find({"user": {"$ne": user_name}})

def add_message(collection_obj, user_name, message, timestamp):
  """
  Adds a message document to the database.
  Returns the timestamp of the document if the transaction was successful.
  """
  document = {
    "user": user_name,
    "content": message,
    "timestamp": timestamp
  }
  x = collection_obj.insert_one(document)
  return x.inserted_id.generation_time

def create_keyword_category(collection_keywords, new_keyword_category, first_keyword):
  """
  Creates a new keyword document populated with an intital keyword. More can be added later

  new_keyword_category -- refers to the general idea (i.e. "Homework").

  first_keyword -- is the first keyword to populate the document (i.e. "hw" and "homework").

  Returns the timestamp of the document if the transaction was successful.
  """
  document = {
    "category": new_keyword_category,
    "keywords": [first_keyword]
  }
  x = collection_keywords.insert_one(document)
  return x.inserted_id.generation_time

def add_keyword(collection_keywords, existing_keyword_category, new_keyword):
  """
  Adds a keyword to an existing keyword document

  new_keyword -- the keyword you want to add (i.e. "hw" and "homework").

  Returns nothing.
  """
  collection_keywords.update_one(
    {"category": existing_keyword_category},
    {"$push": { "keywords": new_keyword}}
  )

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
  client = connect_to_mongo(user, pswd)
  # Gets a database (fast)
  test_server_db = get_db(client, db_name)
  # Gets a collection of data (fast)
  keywords_collection = get_collection(test_server_db, "keywords")
  # Gets and prints out the messages in the collection (fast)
  keywords = get_keywords(keywords_collection)
  for w in keywords:
    print(w)

"""
This is just some code for testing.
If you want to test anything, just uncomment main()
"""

# main()
