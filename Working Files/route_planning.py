<<<<<<< Updated upstream
class Route:
    
    # The route for testing on 17/11
    route = ['f', 'l', 'f', 'r', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'r', 'f', 'r', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'r', 'f', 'l', 's']
=======
from utime import ticks_ms

class Route:   
>>>>>>> Stashed changes
    # No attributes to initialise - yet!
    def __init__(self):
        #Map = Graph()
        # The route for testing on Monday
        self.route = ['f', 'l', 'f', 'r', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'r', 'f', 'r', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'r', 'f', 'l', 's']
    
    # Called when we reach an intersection (when front sensors detect something) to check what to do
    def intersection(self):
        instruction = self.route.pop(0) # Next instruction in the route
        if instruction == 'f':
            return "forwards"     # forwards
        elif instruction == 'b':
            return "backwards"    # reverse
        elif instruction == 't':
            return "turn"         # Turn 180 deg
        elif instruction == 'l':
            return "left" 
        elif instruction == 'r':
            return "right"
        elif instruction == 's':
            return "stop"
        else:
            return "stop"

class Graph:
              
    def __init__(self):
        self.Vertices = ["Start", "IS", "Yellow", "IY", "Red", "IR", "Green", "IG", "Blue", "IB",
                         "ILL-1", "BLL-1",  "ILL-2", "BLL-2", "ILL-3", "BLL-3", "ILL-4", "BLL-4", "ILL-5", "BLL-5", "ILL-6", "BLL-6", "PLL-1",
                         "ILR-1", "BLR-1",  "ILR-2", "BLR-2", "ILR-3", "BLR-3", "ILR-4", "BLR-4", "ILR-5", "BLR-5", "ILR-6", "BLR-6", "PLR-1",
                         "PLL-2", "PLR-2", "ILM", "IUM", "PUL-1", "PUR-1", 
                         "IUL-1", "BUL-1",  "IUL-2", "BUL-2", "IUL-3", "BUL-3", "IUL-4", "BUL-4", "IUL-5", "BUL-5", "IUL-6", "BUL-6", "PUL-2",
                         "IUR-1", "BUR-1",  "IUR-2", "BUR-2", "IUR-3", "BUR-3", "IUR-4", "BUR-4", "IUR-5", "BUR-5", "IUR-6", "BUR-6", "PUR-2"]
        self.NumVertices = 68
        self.AdjacencyMatrix = [ [0 for i in range(68)] for j in range(68)]
        
        # The following code sets up the adjacencyMatrix adding all the edges
        
        for i in range(0, 9, 2):
            self.addEdge(i, i+1)  # Add the lengths from the 5 bays to the line
        for i in range(1, 9, 2):
            self.addEdge(i, i+2)  # Add the lengths across the lines in front of the bays
        self.addEdgeVertices("IR", "ILL-1")
        self.addEdgeVertices("IB", "ILR-1")
        for i in range(10, 22, 2):
            self.addEdge(i, i+1)  # Connect the lower left bays to the line
            self.addEdge(i, i+2)  # Connect the lower left line together
        self.addEdgeVertices("PLL-1", "PLL-2")
        self.addEdgeVertices("PLL-2", "ILM")
        for i in range(23, 35, 2):
            self.addEdge(i, i+1)  # Connect the lower right bays to the line
            self.addEdge(i, i+2)  # Connect the lower right line together
        self.addEdgeVertices("PLR-1", "PLR-2")
        self.addEdgeVertices("PLR-2", "ILM")
        
        self.addEdgeVertices("ILM", "IUM")
        
        self.addEdgeVertices("IUM", "PUL-1")
        self.addEdgeVertices("PUL-1", "IUL-1")
        for i in range(42, 54, 2):
            self.addEdge(i, i+1)  # Connect the upper left bays to the line
            self.addEdge(i, i+2)  # Connect the upper left line together
        self.addEdgeVertices("IUM", "PUR-1")
        self.addEdgeVertices("PUR-1", "IUR-1")
        for i in range(55, 67, 2):
            self.addEdge(i, i+1)  # Connect the upper right bays to the line
            self.addEdge(i, i+2)  # Connect the upper right line together
        
    
    def get_Vertices(self):
        return self.Vertices.copy()
    
    def get_NumVertices(self):
        return self.NumVertices + 0
    
    def get_AdjMatrix(self):
        return self.AdjacencyMatrix.copy()
        
    def addEdge(self, i1, i2):
        self.get_AdjMatrix()[i1][i2] = 1
        self.get_AdjMatrix()[i2][i1] = 1
        
    def addEdgeVertices(self, v1, v2):
        index1 = self.get_Vertices().index(v1)
        index2 = self.get_Vertices().index(v2)
        self.addEdge(index1, index2)
        
    def getDistance(self, vertex1, vertex2):
        index1 = self.get_Vertices().index(vertex1)
        index2 = self.get_Vertices().index(vertex2)
        return self.get_AdjMatrix()[index1][index2]
        
    def dijkstra(self, startVertex, endVertex):
        minDistances = {vertex:10e8 for vertex in self.get_Vertices()}       # Set up to the minimum distances from the start vertex, initially basically infinite
        previousVertex = {vertex:"" for vertex in self.get_Vertices()}       # Set up the previous vertex dictionary, the previous vertex in the route
        verticesLeftToVisit = self.get_Vertices()                            # Set up the list of vertices left to visit - finished when this is emptied
            
        verticesLeftToVisit.remove(startVertex)        # Do the starting vertex
        minDistances[startVertex] = 0
        startIndex = self.get_Vertices().index(startVertex)

        for i in range(0, self.get_NumVertices()):                # Find all the vertices directly connected to the start vertex and set the distances based on edge weight
            if self.get_AdjMatrix()[startIndex][i] != 0:
                vertex = self.get_Vertices()[i]
                minDistances[vertex] = self.get_AdjMatrix()[startIndex][i]
                previousVertex[vertex] = startVertex
                
        while len(verticesLeftToVisit) > 0:            # Repeat while there are still vertices left to visit:
            minVertexDistance = 10e8
            for v in verticesLeftToVisit:              # Find the vertex with the smallest distance from the start that hasn't already been visited
                if minDistances[v] < minVertexDistance:
                    currentVertex = v
                    minVertexDistance = minDistances[v]
            verticesLeftToVisit.remove(currentVertex)                  # Visit the currentVertex by removing it from this list and looking at vertices connected to it
            currentIndex = self.get_Vertices().index(currentVertex)
            
            if currentVertex == endVertex:                             # Once we reach the end vertex there's no point visiting the others
                break
            
            for i in range(0, self.get_NumVertices()):              
                if self.get_AdjMatrix()[currentIndex][i] != 0:              # Find all the vertices directly connected to the current vertex
                    vertex = self.get_Vertices()[i]
                    distanceFromStart = self.get_AdjMatrix()[currentIndex][i] + minDistances[currentVertex]
                    if minDistances[vertex] > distanceFromStart:                          # If the distance to the start of this node is shorter going via currentNode, include it
                        minDistances[vertex] = distanceFromStart
                        previousVertex[vertex] = currentVertex
            
        vertexRoute = [endVertex]
        while vertexRoute[0] != startVertex:              # Go backwards through the previousVertex dictionary to trace the route back to the start
            newVertex = previousVertex[vertexRoute[0]]
            vertexRoute = [newVertex] + vertexRoute       # Add the 'next' vertex to the start of the list as we are going backwards from the end
            
        return vertexRoute, minDistances[endVertex]      
            
        
        
        
t1 = ticks_ms()
route = Route()
graph = Graph()
t2 = ticks_ms()
print(t2 - t1)

t1 = ticks_ms()
print(graph.dijkstra("Start", "PUR-2"))
t2 = ticks_ms()
print(t2 - t1)