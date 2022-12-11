
import geopy.distance
import DBManager

#Source and dest are iata codes. 
def updateDistance():
    #retrieves all the routes from the database
    routesFull = DBManager.retrieve_records("routes", None)
    airportsFull = DBManager.retrieve_records("airports", None)

    DBManager.reset_database("routes")

    returnArray = []

    for route in routesFull:
        try:
            sourceairport = list(filter(lambda airport: (airport['iata'] == route['sourceairport']), airportsFull))[0]
            destinationairport = list(filter(lambda airport: (airport['iata'] == route['destinationairport']), airportsFull))[0]
            route["distance"] = geopy.distance.geodesic((sourceairport["latitude"], sourceairport["longitude"]),(destinationairport["latitude"], destinationairport["longitude"])).km
            returnArray.append(route)
        except:
            continue

    DBManager.add_documents("routes", routesFull)

