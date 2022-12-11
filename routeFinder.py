import DBManager
from queue import Queue
import timeit


def findRoute(dest, source, weightList, privList):
    path = []

    current = dest
    priv = str()

    max_hops = 5
    itr = 0

    while(itr <= 5):
        if (current == source):
            path.append(current)
            break
        if (current not in privList.keys()):
            print(str(current), " Not in result")
            break
        print(current, " ", privList[current])
        path.append(current)
        current = privList[current]
        itr += 1

    path.reverse()
    return path, weightList[dest]

    

#Source and dest are iata codes. 
def getRoute(source, dest):

    routeDocument = DBManager.retrieve_records("PredeterminedRoutes", {"Source Airport": source})

    if routeDocument != []:

        results = findRoute(dest, source, routeDocument["weight_list"], routeDocument["priv_list"])


    else:

        #retrieves all the routes from the database
        routesFull = DBManager.retrieve_records("routes", {"distance": {"$exists": True}})

        #Builds a graph/tree with the queried data 
        tree = Graph()

        for route in routesFull:
            tree.add_edge(route['sourceairport'], route['destinationairport'], route['distance'])

        bfs_nodes = tree.find_possible_paths(source, dest, [], 3)

        print(bfs_nodes)

        dtree = dijkstrasGraph()
        for route in routesFull:
            if (route['sourceairport'] in bfs_nodes[0] and route['destinationairport'] in bfs_nodes[0]):
                dtree.add_edge(route['sourceairport'], route['destinationairport'], route['distance'])


        dijkstrasResult = dtree.dijkstras(source)

        results = findRoute(dest, source, dijkstrasResult[0], dijkstrasResult[1])


    print("resultsare")
    print(results)

    final_return = []

    previous_ap = ""
    for ap in results[0]:
        if previous_ap == "":
            previous_ap = ap
        else:
            routeInfo = [DBManager.retrieve_records("routes", {"sourceairport": previous_ap, "destinationairport": ap})[0]]
            previous_ap = ap


            final_return.append(routeInfo)

    return final_return
            


#Class that creates and searches a graph.
class Graph:
    def __init__(self):
        self.adjlist = {}


    def add_edge(self, node1, node2, weight=1, distance=None):
        if node1 not in self.adjlist.keys():
            self.adjlist[node1] = {node2 : {"stops" : weight, "distance": distance}}
        if node2 not in self.adjlist.keys():
            self.adjlist[node2] = {}
        self.adjlist[node1][node2]= {"stops" : weight, "distance": distance}



    
    def find_possible_paths(self, start, target, path, depth):

        return_paths = []

        currentpath = path.copy()
        print("CURRENTPATH")
        print(currentpath)

        if start in currentpath:
            return []

        currentpath.append(start)

        if depth == 0:
            return []

        if start == target:
            tempPath = currentpath.copy()
            tempPath.append(start)
            return_paths.append(currentpath)

        for route in self.adjlist[start]:
            print(route)
            if route not in currentpath:
                recursive_response = self.find_possible_paths(start, target, currentpath, depth-1)
                print(recursive_response)
                return_paths += recursive_response.copy()

        return return_paths


#Class that creates and searches a graph.
class dijkstrasGraph:
    def __init__(self):
        self.adjlist = {}

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
    