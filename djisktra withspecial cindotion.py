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
    F = Vertex('F')
    G = Vertex('G')

    # Create edges
    A.edges.append(Edge(B, 4))
    B.edges.append(Edge(A, 3))  # Bidirectional edge
    A.edges.append(Edge(C, 3))  # Unidirectional edge
    A.edges.append(Edge(D, 3))  # Unidirectional edge
    B.edges.append(Edge(E, 4))  # Unidirectional edge
    C.edges.append(Edge(F, 2))
    F.edges.append(Edge(C, 2))  # Bidirectional edge
    D.edges.append(Edge(G, 1))  # Unidirectional edge
    E.edges.append(Edge(G, 3))  # Unidirectional edge
    F.edges.append(Edge(G, 1))
    G.edges.append(Edge(F, 2))  # Bidirectional edge

    # Create graph and add vertices
    graph = Graph()
    graph.add_vertex(A)
    graph.add_vertex(B)
    graph.add_vertex(C)
    graph.add_vertex(D)
    graph.add_vertex(E)
    graph.add_vertex(F)
    graph.add_vertex(G)

    # Get shortest path from A to G
    distance, path = graph.get_shortest_path(B, G)
    print(f"The shortest path from B to G is {path} with a total weight of {distance}")
