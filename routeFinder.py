import DBManager
from queue import Queue
import timeit

def GetRoute(source, dest, max_depth=5):

    '''
    routesFull, routeDests = GetRouteInfo(source)
    destinfo = DBManager.retrieve_records("airports", {'icao': dest})
    destid =  destinfo[0].get("airportid")
    destiata = destinfo[0].get("iata")
    destcheck = [destiata, destid]
    
    '''
    routesFull = DBManager.retrieve_records("routes", None)
    
    routeDests = []

    for x in routesFull:
        des = [x.get('destinationairport'), x.get('destinationairportid')]
        if des not in routeDests:
            routeDests.append(des)

    tree = BuildTree(routesFull, routeDests)

    start = timeit.default_timer()
    path = tree.bfs('SEA', 'DUB')
    stop = timeit.default_timer()
    print(path)
    print("Time Taken: ", stop - start)
    

def BuildTree(routesFull, routedest):
    tree = Graph(len(routedest))

    for x in routesFull:
        tree.add_edge(x.get('sourceairport'), x.get('destinationairport'), x.get('stops')+1)
    
    #tree.print_adj_list()
        
    return tree

def GetRouteInfo(source, max_depth=3):
    

    sourceinfo = DBManager.retrieve_records("airports", {'icao': source})
    sourceid =  sourceinfo[0].get("airportid")

    #print(sourceid)

    routes1 = DBManager.retrieve_records("routes", {'sourceairportid': str(sourceid)})

    #print(routes1)
    posDest = []

    for x in routes1:
        des = [x.get('destinationairport'), x.get('destinationairportid')]
        if des not in posDest:
            posDest.append(des)

    depth = 0
    while(depth <= max_depth):
        qArray = []
        for n in posDest:
            qArray.append(str(n[1]))
        routes1 = routes1 + DBManager.retrieve_records("routes", {'sourceairportid':{ '$in':qArray}})

        for x in routes1:
            des = [x.get('destinationairport'), x.get('destinationairportid')]
            if des not in posDest:
                posDest.append(des)
        depth += 1

    return routes1, posDest



class Graph:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.m_nodes = range(self.num_nodes)
        self.adjlist = {}

    def add_edge(self, node1, node2, weight=1):
        if node1 not in self.adjlist.keys():
            self.adjlist[node1] = [(node2, weight)]
        self.adjlist[node1].append((node2, weight))

    def print_adj_list(self):
        for key in self.adjlist.keys():
            print("node", key, ": ", self.adjlist[key])
    
    def dfs (self, start, target, path = [], visited = set()):
        path.append(start)
        visited.add(start)

        if start == target:
            print(path)
            
        if start  in self.adjlist.keys():
            for (neighbor, weight) in self.adjlist[start]:
                if neighbor not in visited:
                    result, back = self.dfs(neighbor, target, path, visited)
                    if result is not None:
                        return result
        path.pop()
        return None
    
    def bfs(self, start, target):
        
        visited = set()
        queue = Queue()

        queue.put(start)
        visited.add(start)

        parent = dict()

        parent[start] = None

        path_found = False

        while not queue.empty():
            current = queue.get()
            if current == target:
                path_found = True
                break
            
            if start  in self.adjlist.keys():
                for (next, weight) in self.adjlist[current]:
                    if next not in visited:
                        queue.put(next)
                        parent[next] = current
                        visited.add(next)
        path = []
        if path_found:
            path.append(target)
            while parent[target] is not None:
                path.append(parent[target])
                target = parent[target]
            path.reverse()
        return path



    