import DBManager
import datetime

def importRoutes():
    routesFull = DBManager.retrieve_records("routes", {"distance": {"$exists": True}})
    return routesFull

def setupGraph(graph, routes):
    for route in routes:
        graph.add_edge(route['sourceairport'], route['destinationairport'], route['distance'])
    
    return graph


def savetoDatabase(weightList, privList, source):
    DBManager.add_documents("PredeterminedRoutes", [{"Source_Airport" : source, "weight_list": weightList, "priv_list": privList, "timestamp": datetime.datetime.now()}])


#Pass in a list of iata codes. This function will use calls to build a dijkstra shortest path table and save the table into the database
def predetermineRoutesDriver(sources):
    allRoutes = importRoutes()
    graph = dijkstrasGraph()
    graph = setupGraph(graph, allRoutes)
    for x in sources:
        predetermineRoutes(x, graph)
    

#runs dijkstra's and saves result to database
def predetermineRoutes(source, graph):
    
    result = graph.dijkstras(source)
    savetoDatabase(result[0], result[1], source)
    
    

#finds route in database
def pullRouteFromDatabase(dest, source):

    result = DBManager.retrieve_records("PredeterminedRoutes", {"Source_Airport" : str(source)})[0]
    if not result:
        print("No entry found for this request: ", source)
        return None, 0
    path, w = findRoute(dest, source, result["weight_list"], result['priv_list'])
    return path, w

#finds shortest route using dijkstras priv list
def findRoute(dest, source, weightList, privList):
    path = []

    current = dest
    priv = str()

    max_hops = 5
    itr = 0

    while(itr <= 5):
        if (current == source):
            break
        if (current not in privList.keys()):
            print(str(current), " Not in result")
            break
        print(current, " ", privList[current])
        path.append(privList[current])
        current = privList[current]
        itr += 1

    return path.reverse(), weightList[dest]

    


#Class that creates and searches a graph.
class dijkstrasGraph:
    def __init__(self):
        self.adjlist = dict()

    def add_edge(self, node1, node2, weight=1):
        if node1 not in self.adjlist.keys():
            self.adjlist[node1] = {node2 : {"weight" : weight}}
        if node2 not in self.adjlist.keys():
            self.adjlist[node2] = {}
        self.adjlist[node1][node2]= {"weight" : weight}


    def dijkstras(self, start):

        visited = []
        queue = []
        weight = {}
        previous = {}

        for node in self.adjlist.keys():
            weight[node] = 99999999
            previous[node] = None
            queue.append(node)

        weight[start] = 0

        currentnode = start

        while queue != []:

            sortedWeight = (sorted(weight.items(), key=lambda x: x[1]))

            for path in sortedWeight:
                if path[0] in visited:
                    continue


                currentnode = path[0]
                break

            for (node, data) in sorted(self.adjlist[currentnode].items(), key=lambda x: x[1]["weight"]):
                if node in visited:
                    continue

                temp_distance_value = data["weight"] + weight[currentnode]

                if weight[node] > temp_distance_value:
                    previous[node] = currentnode
                    weight[node] = temp_distance_value

            queue.remove(currentnode)
            visited.append(currentnode)


        return([weight, previous])