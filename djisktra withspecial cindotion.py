import heapq

class Vertex:
    def __init__(self, name):
        self.name = name
        self.visited = False
        self.discovered = False
        self.time_to_reach = float('inf')
        self.edges = []
        self.previous_vertex = None  # Add this line

    def __lt__(self, other):
        return self.time_to_reach < other.time_to_reach

class Edge:
    def __init__(self, to_vertex, weight):
        self.to_vertex = to_vertex
        self.weight = weight

class Graph:
    def __init__(self):
        self.vertices = []

    def add_vertex(self, vertex):
        self.vertices.append(vertex)


    def dijkstra(self, start_vertex):
        queue = []
        start_vertex.time_to_reach = 0
        heapq.heappush(queue, start_vertex)

        while queue:
            current_vertex = heapq.heappop(queue)
            current_vertex.visited = True

            for edge in current_vertex.edges:
                if not edge.to_vertex.visited:
                    tentative_distance = current_vertex.time_to_reach + edge.weight
                    if tentative_distance < edge.to_vertex.time_to_reach:
                        edge.to_vertex.time_to_reach = tentative_distance
                        edge.to_vertex.discovered = True
                        edge.to_vertex.previous_vertex = current_vertex
                        heapq.heappush(queue, edge.to_vertex)

    def get_shortest_path(self, start_vertex, end_vertex):
        self.dijkstra(start_vertex)
        path = []
        current_vertex = end_vertex

        while current_vertex is not None:
            path.append(current_vertex.name)
            current_vertex = current_vertex.previous_vertex

        path.reverse()
        return end_vertex.time_to_reach, path

if __name__ == "__main__":
    # Create vertices
    A = Vertex('A')
    B = Vertex('B')
    C = Vertex('C')
    D = Vertex('D')
    E = Vertex('E')

    # Create edges
    A.edges.append(Edge(B, 0))
    B.edges.append(Edge(A, 1))
    A.edges.append(Edge(C, 3))
    C.edges.append(Edge(A, 2))
    B.edges.append(Edge(D, 1))

    C.edges.append(Edge(E, 4))
    E.edges.append(Edge(C, 1))
    D.edges.append(Edge(C, 1))


    # Create graph and add vertices
    graph = Graph()
    graph.add_vertex(A)
    graph.add_vertex(B)
    graph.add_vertex(C)
    graph.add_vertex(D)
    graph.add_vertex(E)

    # Get shortest path from A to E
    distance, path = graph.get_shortest_path(B, E)
    print(f"The shortest path from A to E is {path} with a total weight of {distance}")
