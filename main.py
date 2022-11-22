try:
  from asyncio.windows_events import NULL
except ImportError:
  import asyncio
from doctest import Example
import pymongo
import dns
import json
import pandas
import requests
import datetime
import time

def connect_and_return_cluster_connection():
  #connect and authenticate to database
  client = pymongo.MongoClient("mongodb+srv://ssenjieh:beans@cluster0.3tfslgn.mongodb.net/?retryWrites=true&w=majority")
  cluster = client.teambullfrog

  return cluster

#connect and return the pointer essentially to mongodb atlas collection(database)
def connect_and_return_db_connection(database_name):

  cluster = connect_and_return_cluster_connection()

  #connect to client and make db reference to correct collection(table) aka database
  try:
    db = NULL

    match database_name:
      case "airports":
        db = cluster.airports
      case "airlines":
        db = cluster.airlines
      case "routes":
        db = cluster.routes
      case "planes":
        db = cluster.planes
      case "countries":
        db = cluster.countries
      case "arrival":
        db = cluster.arrival

    if db == NULL:
      db = eval("cluster." + str(database_name))

  except:
    return False

  return db

#add document to database based on specified db and input data
#input data can be a json dict or an array of json dicts
def add_documents(database_name, input_data):

  db = connect_and_return_db_connection(database_name)

  #send request to mongo
  if type(input_data) is dict:
    db.insert_one(input_data)
  
  #of or if there are mutiple documents to send
  elif type(input_data) is list:
    db.insert_many(input_data)

#add a new database to store any items for any future methods we need to develop
def add_new_database(database_name):

  cluster = connect_and_return_cluster_connection()

  try:
    cluster.create_collection(database_name)
  except:
    return False

  return True

def drop_database(database_name):

  db = connect_and_return_db_connection(database_name)

  try:
    db.drop()
  except:
    return False

  return True

#give records from db(database) based on specifiers defined by a dict of key:value pairs
#specifier examples:
# {'job.title': 'programmer'}
# find documents have field value that is not equal to a specific value
# {field: {$ne: 'string is also accepted in some operators'}} 
# other operators that can be used instead of $ne and what they mean
#   $all
#   $in
#   $gte
#   $gt
#   $lt
#   $lte
#plenty more information on other operators in this cheatsheet:
# https://github.com/mhmda-83/mongodb-cheatsheet

def retrieve_records(database_name, specifiers):

  #connect to the database
  db = connect_and_return_db_connection(database_name)

  #find all values that match the specifier rules and attach to cursor variable
  cursor = db.find(specifiers)

  #make a return array that gives an array of json dicts from the return cursor
  return_array = []

  #iterate through each and add to return array
  #note that we have to do for loop through the cursor as the find function gives us a cursor not a return list
  #this is what we have to do to make it a return list of json dicts that represent what we're looking for
  for document in cursor:
    return_array.append(document)
    
  #return return array
  return return_array

#list all databases in the main cluster
def list_databases():

  #connect to the database
  cluster = connect_and_return_cluster_connection()

  #list databases
  try:
    database_list = cluster.list_collection_names()
  except:
    False

  #return value
  return database_list

#update database record based on specifiers similar to retrieve documents
#specifier examples:
#   
# other operators that can be used
#   $inc - increment value up
#   $push - push value into an array
#   $set - set value of field to specific value
#plenty more information on other operators in this cheatsheet:
# https://github.com/mhmda-83/mongodb-cheatsheet

def update_records(database_name, specifiers, opval):

  #connect to the database
  db = connect_and_return_db_connection(database_name)

  #find all values that match the specifier rules and attach to cursor variable
  try:
    db.update(specifiers, opval)
  except:
    return False

  #return return array
  return True

#incase of some sort of catastrophic failure we can run this to reset the databases listed in the database.json database list
def reset_databases():

  #connects to the cluster to allow us to add or remove databases
  cluster = connect_and_return_cluster_connection()

  #open the database list config file
  with open('databases.json') as f:
   data = json.load(f)
  
  #iterate through each of the recorded database files from the config file
  for i in data:

    #try to connect to the database and drop it if not it probably doesn't exist and we can pass
    try:
      connect_and_return_db_connection(i).drop()
    except:
      pass

    #recreate the database
    cluster.create_collection(i)

    #read the info from local version of database
    csvfile = pandas.read_csv("local_data//" + str(i) + ".csv")

    #create an array to let us pass into the add documents file which can either accept a json dict or an array of json dicts
    input_data = []

    #iterate through the local version database that was read with pandas
    #note that pandas was used as there are char types that aren't within the scope of UTF characters and would
    # break csvreader
    for index, row in csvfile.iterrows():
      #make the dict that represents the record being iterated through
      append_dict = {}

      #attach each of the values
      try:
        for key in csvfile.columns:
          append_dict[key] = row[key]
      except:
        pass

      #add that to the input array of dicts
      input_data.append(append_dict)

    #add the input array of dicts into the new database
    add_documents(i, input_data)

def get_and_set_data(dataName, url):
  # Add the data to the database
  add_new_database(dataName)

  # Add recent arrivals to the arrival database
  if dataName == "arrival":
    response = requests.get(url)
    add_documents(dataName, response.json())

def main_example():
  #add a new database
  add_new_database("random_example_database")

  #check all existing databases
  print(list_databases())

  #add some document examples 

  #single document
  add_documents("random_example_database", {"example_key" : "example_val", "some_other_key": 400})

  #mutiple documents at once
  add_documents("random_example_database", [{"example_key" : "example_val2", "some_other_key": 300}, 
                                            {"example_key" : "example_val3", "some_other_key": 200}, 
                                            {"example_key" : "example_val4", "some_other_key": 100}, 
                                            {"example_key" : "example_val5", "some_other_key": 0}])

  #retrieve documents with key value pair 
  print(retrieve_records("random_example_database" , {"example_key" : "example_val"}))

  #retrieve documents with value greater than 100 for specific key
  print(retrieve_records("random_example_database" , {"some_other_key" : {"$gt" : 100}}))

  #retrieve all documents from database
  print(retrieve_records("random_example_database" , None))

  #drop the database
  drop_database("random_example_database")

  #list databases again
  print(list_databases())


def main():
  # Get the current day
  current_time = datetime.datetime.now()
  today_began = str(time.mktime(datetime.date(current_time.year, current_time.month, current_time.day).timetuple()))
  month_ago_began = str(int(float(today_began)) - (86400 * 30))

  # Temperary Airport ID value
  airportID = "EDDF"

  # Example of getting arrival information for an airport and storing it in the database
  get_and_set_data("arrival", f"https://opensky-network.org/api/flights//arrival?airport={airportID}&begin={int(float(today_began))}&end={int(month_ago_began)}")

  #list databases again
  print(list_databases())

# __name__
if __name__=="__main__":
    main()