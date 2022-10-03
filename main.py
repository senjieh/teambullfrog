import mysql.connector

#connect to local mysql
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1101",
)

#create database with database name
def create_database(database_name):

  #create cursor to execute create db command
  createdbcursor = mydb.cursor()
  
  #try creating database if error occurs return False
  try:
    createdbcursor.execute("CREATE DATABASE" + str(database_name))
  except:
    return False
  
  return True


def database_init():

  #create cursor to parse through available databases
  showdatabasecursor = mydb.cursor()

  showdatabasecursor.execute("SHOW DATABASES")

  #loop through dbs to see if one matches
  for database in showdatabasecursor:
    if str(database) == "('openflightsdb',)":
      print(database)
      return True

  #if no dbs match openflightsdb create one and return True
  if create_database('openflightsdb') == True:
    return True
  else:
    return False

# Defining main function
def main():
    #initialize database
    database_init()
  
  
# Using the special variable 
# __name__
if __name__=="__main__":
    main()