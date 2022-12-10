
import DBManager
import routeFinder

def main():


  #check all existing databases
  print(DBManager.list_databases())

  #add some document examples 
  '''
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
  '''
  #print(DBManager.retrieve_records("routes", {'sourceairportid':{ '$in':['3577', '3550']}}))

  #list databases again
  #print(list_databases())

  #routeFinder.BuildRouteTree("KSEA", "DEN")

  routeFinder.GetRoute('KSEA', 'KDEN')


# __name__
if __name__=="__main__":
    main()