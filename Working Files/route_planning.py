class Route:   

    def __init__(self, startVertex, endVertex):
        self.graph = Graph()
        self.vertexRoute, self.instructions = self.graph.plan_route(startVertex, endVertex)
        self.currentPosition = startVertex
    
    def get_currentPosition(self):
        return self.currentPosition
    
    # Called when we reach an intersection (when front sensors detect something) to check what to do
    def intersection(self):
        self.currentPosition = self.vertexRoute.pop(0)  # Now in new position, as given by the route
        instruction = self.instructions.pop(0)     # Next instruction in the route

class Route:   

    def __init__(self, startVertex, endVertex):
        graph = Graph()
        self.vertexRoute, self.instructions = self.graph.dijkstra(startVertex, endVertex)
        self.currentPosition = self.vertexRoute.pop(0)
        # The route for the line sensing teston 17/11
        #self.route = ['f', 'l', 'f', 'r', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'r', 'f', 'r', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'r', 'f', 'l', 's']
    
    # Called when we reach an intersection (when front sensors detect something) to check what to do
    def intersection(self):
        instruction = self.route.pop(0) # Next instruction in the route

        if instruction == 'f':
            return "forwards"
        elif instruction == 'b':
            return "backwards"
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
        self.DistanceMatrix = [ [0 for i in range(68)] for j in range(68)]
        self.DirectionMatrix = [ [" " for i in range(68)] for j in range(68)]
        
        # The following code sets up the distance matrix adding all the edges
        # It also sets up the direction matrix to get the direction instruction between 2 nodes
        # DO NOT CHANGE UNLESS YOU UNDERSTAND IT!
        
        # FRONT BAYS
        for i in range(0, 9, 2):
            self.addEdge(i, i+1, 35)  # Add the lengths from the 5 bays to the line
        
        self.addDirectionVertices("Start", "IY", 'l')
        self.addDirectionVertices("Start", "IG", 'r')
        self.addDirectionVertices("IS", "Yellow", 'l')
        self.addDirectionVertices("IS", "Green", 'r')
        self.addDirectionVertices("IS", "IR", 'f')
        self.addDirectionVertices("IS", "IB", 'f')
        
        self.addDirectionVertices("Yellow", "IR", 'l')
        self.addDirectionVertices("Yellow", "IS", 'r')
        self.addDirectionVertices("IY", "Red", 'l')
        self.addDirectionVertices("IY", "Start", 'r')
        self.addDirectionVertices("IY", "ILL-1", 'r')
        self.addDirectionVertices("Red", "ILL-1", 'f')
        self.addDirectionVertices("Red", "IY", 'r')
        self.addDirectionVertices("IR", "Yellow", 'r')
        self.addDirectionVertices("IR", "BLL-1", 'r')
        self.addDirectionVertices("IR", "ILL-2", 'f')
        
        self.addDirectionVertices("Green", "IS", 'l')
        self.addDirectionVertices("Green", "IB", 'r')
        self.addDirectionVertices("IG", "Start", 'l')
        self.addDirectionVertices("IG", "Blue", 'r')
        self.addDirectionVertices("IG", "ILR-1", 'l')
        self.addDirectionVertices("Blue", "IG", 'l')
        self.addDirectionVertices("Blue", "ILR-1", 'f')
        self.addDirectionVertices("IB", "Green", 'l')
        self.addDirectionVertices("IB", "BLR-1", 'l')
        self.addDirectionVertices("IB", "ILR-2", 'f')
        
        self.addEdgeVertices("IS", "IY", 73)
        self.addEdgeVertices("IY", "IR", 29)
        self.addEdgeVertices("IS", "IG", 73)
        self.addEdgeVertices("IG", "IB", 29)
        
        self.addEdgeVertices("IR", "ILL-1", 71)
        self.addEdgeVertices("IB", "ILR-1", 71)
        
        # LOWER LEFT
        for i in range(10, 22, 2):
            if i < 20:
                self.addDirection(i, i+3, 'r')
                self.addDirection(i, i+4, 'f')
            self.addEdge(i, i+1, 21)  # Connect the lower left bays to the line
            self.addEdge(i, i+2, 7)   # Connect the lower left line together
        
        self.addDirectionVertices("ILL-6", "PLL-2", 'f')
        self.addDirectionVertices("PLL-1", "ILM", 'r')
        self.addDirectionVertices("PLL-2", "IUM", 'r')
        
        self.addEdgeVertices("PLL-1", "PLL-2", 37)
        self.addEdgeVertices("PLL-2", "ILM", 102)
        
        # LOWER RIGHT
        for i in range(23, 35, 2):
            if i < 33:
                self.addDirection(i, i+3, 'l')
                self.addDirection(i, i+4, 'f')
            self.addEdge(i, i+1, 21)  # Connect the lower right bays to the line
            self.addEdge(i, i+2, 7)   # Connect the lower right line together
        
        self.addDirectionVertices("ILR-6", "PLR-2", 'f')
        
        self.addDirectionVertices("PLR-1", "ILM", 'l')
        self.addDirectionVertices("PLR-2", "IUM", 'l')
        
        self.addEdgeVertices("PLR-1", "PLR-2", 37)
        self.addEdgeVertices("PLR-2", "ILM", 102)
        
        # MIDDLE
        self.addEdgeVertices("ILM", "IUM", 137)
        
        self.addDirectionVertices("ILM", "PUL-1", 'r')
        self.addDirectionVertices("ILM", "PUR-1", 'l')
        
        # UPPER LEFT
        self.addDirectionVertices("IUM", "IUL-1", 'r')
        self.addDirectionVertices("PUL-1", "IUL-2", 'f')
        
        self.addEdgeVertices("IUM", "PUL-1", 43)
        self.addEdgeVertices("PUL-1", "IUL-1", 34)
        
        for i in range(42, 54, 2):
            if i < 52:
                self.addDirection(i, i+3, 'l')
                self.addEdge(i, i+2, 7)        # Connect the upper left line together
                self.addDirection(i, i+4, 'f')
            self.addEdge(i, i+1, 21)  # Connect the upper left bays to the line
        
        self.addDirectionVertices("IUL-5", "PUL-2", 'f')
        self.addEdgeVertices("IUL-6", "PUL-2", 10)
        self.addDirectionVertices("IUL-6", "IUL-6", 't')
        
        # UPPER RIGHT
        self.addDirectionVertices("IUM", "IUR-1", 'l')
        self.addDirectionVertices("PUR-1", "IUR-2", 'f')
        
        self.addEdgeVertices("IUM", "PUR-1", 43)
        self.addEdgeVertices("PUR-1", "IUR-1", 34)
        for i in range(55, 67, 2):
            if i < 65:
                self.addDirection(i, i+3, 'l')
                self.addEdge(i, i+2, 7)        # Connect the upper right line together
                self.addDirection(i, i+4, 'f')
            self.addEdge(i, i+1, 21)  # Connect the upper right bays to the line
        
        self.addDirectionVertices("IUR-5", "PUR-2", 'f')
        self.addEdgeVertices("IUR-6", "PUR-2", 10)
        self.addDirectionVertices("IUR-6", "IUR-6", 't')
        

    def get_Vertices(self):
        return self.Vertices.copy()
    
    def get_NumVertices(self):
        return self.NumVertices + 0
    
    def get_DistMatrix(self):
        return self.DistanceMatrix.copy()
    
    def get_DirectionMatrix(self):
        return self.DirectionMatrix.copy()
    
    def getDistance(self, vertex1, vertex2):
        index1 = self.get_Vertices().index(vertex1)
        index2 = self.get_Vertices().index(vertex2)
        return self.get_DistMatrix()[index1][index2]
    
    def getDirection(self, vertex1, vertex2):
        index1 = self.get_Vertices().index(vertex1)
        index2 = self.get_Vertices().index(vertex2)
        return self.get_DirectionMatrix()[index1][index2]
        
    def addEdge(self, i1, i2, dist):
        self.DistanceMatrix[i1][i2] = dist
        self.DistanceMatrix[i2][i1] = dist
        
    def addEdgeVertices(self, v1, v2, dist):
        index1 = self.get_Vertices().index(v1)
        index2 = self.get_Vertices().index(v2)
        self.addEdge(index1, index2, dist)
        
    def addDirection(self, i1, i2, direction):
        self.DirectionMatrix[i1][i2] = direction
        if direction == "l":
            direction = "r"
        elif direction == "r":
            direction = "l"
        self.DirectionMatrix[i2][i1] = direction
        
    def addDirectionVertices(self, v1, v2, direction):
        index1 = self.get_Vertices().index(v1)
        index2 = self.get_Vertices().index(v2)
        self.addDirection(index1, index2, direction)
        self.get_AdjMatrix()[i1][i2] = 1
        
    def dijkstra(self, startVertex, endVertex):
        minDistances = {vertex:10e8 for vertex in self.get_Vertices()}       # Set up to the minimum distances from the start vertex, initially basically infinite
        previousVertex = {vertex:"" for vertex in self.get_Vertices()}       # Set up the previous vertex dictionary, the previous vertex in the route
        verticesLeftToVisit = self.get_Vertices()                            # Set up the list of vertices left to visit - finished when this is emptied
            
        verticesLeftToVisit.remove(startVertex)        # Do the starting vertex
        minDistances[startVertex] = 0
        startIndex = self.get_Vertices().index(startVertex)

        for i in range(0, self.get_NumVertices()):                # Find all the vertices directly connected to the start vertex and set the distances based on edge weight
            if self.get_DistMatrix()[startIndex][i] != 0:
                vertex = self.get_Vertices()[i]
                minDistances[vertex] = self.get_DistMatrix()[startIndex][i]
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

                if self.get_DistMatrix()[currentIndex][i] != 0:              # Find all the vertices directly connected to the current vertex
                    vertex = self.get_Vertices()[i]
                    distanceFromStart = self.get_DistMatrix()[currentIndex][i] + minDistances[currentVertex]
                    if minDistances[vertex] > distanceFromStart:                          # If the distance to the start of this node is shorter going via currentNode, include it
                        minDistances[vertex] = distanceFromStart
                        previousVertex[vertex] = currentVertex
            
        vertexRoute = [endVertex]
        while vertexRoute[0] != startVertex:              # Go backwards through the previousVertex dictionary to trace the route back to the start
            newVertex = previousVertex[vertexRoute[0]]
            vertexRoute = [newVertex] + vertexRoute       # Add the 'next' vertex to the start of the list as we are going backwards from the end
            
<<<<<<< Updated upstream

        return vertexRoute      
            
    def plan_route(self, startVertex, endVertex):
        vertexRoute = self.dijkstra(startVertex, endVertex)
        instructions = []
        if startVertex == "Start":
            instructions = ['f']
        else:
            instructions = ['t']
            
        for i in range(1, len(vertexRoute)-1):
            previousVertex = vertexRoute[i-1]
            nextVertex = vertexRoute[i+1]
            direction = self.getDirection(previousVertex, nextVertex)
            instructions.append(direction)
        
        instructions.append('s')
        
        return vertexRoute, instructions
        
        
route = Route("Start", "IR")
print(route.instructions)
print(route.get_currentPosition())
print(route.intersection())
print(route.intersection())
print(route.get_currentPosition())

