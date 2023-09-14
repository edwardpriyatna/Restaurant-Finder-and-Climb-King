import heapq
class Vertex:
    def __init__(self, name, weight=0):
        self.name = name
        self.visited = False
        self.discovered = False
        self.time_to_reach = float('inf')
        self.edges = []
        self.previous_vertex = None
        self.weight = weight
        self.added_weight = 0

    def __lt__(self, other):
        return self.time_to_reach < other.time_to_reach

    def __str__(self):
        return f"Vertex {self.name}, weight {self.weight}, visited {self.visited}, discovered {self.discovered}, " \
               f"time_to_reach {self.time_to_reach}, edges {[str(edge) for edge in self.edges]}, " \
               f"previous_vertex {self.previous_vertex.name if self.previous_vertex else None}, added_weight {self.added_weight}"


class Edge:
    def __init__(self, to_vertex, weight):
        self.to_vertex = to_vertex
        self.weight = weight

    def __str__(self):
        return f"Edge to {self.to_vertex.name}, weight {self.weight}"


class Graph:
    def __init__(self, edges, weights):
        self.vertices = [Vertex(i) for i in range(max(max(edges, key=lambda x: max(x[:2]))[:2]) + 1)]

        for weight in weights:
            self.vertices[weight[0]].weight = weight[1]

        for edge in edges:
            edge_instance = Edge(self.vertices[edge[1]], edge[2])
            self.vertices[edge[0]].edges.append(edge_instance)

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

    def get_shortest_path(self, start_vertex_index, end_vertex_index):
        start_vertex = self.vertices[start_vertex_index]
        end_vertex = self.vertices[end_vertex_index]
        self.dijkstra(start_vertex)

        if end_vertex.time_to_reach == float('inf'):
            return None

        path = []
        current_vertex = end_vertex

        while current_vertex is not None:
            path.append(current_vertex.name)
            current_vertex = current_vertex.previous_vertex

        path.reverse()
        return end_vertex.time_to_reach, path

    def __str__(self):
        return "\n".join(str(vertex) for vertex in self.vertices)


if __name__ == "__main__":
    # The edges represented as a list of tuples
    edges = [(0, 1, 4), (0, 3, 2), (0, 2, 3), (2, 3, 2), (3, 0, 3)]
    # The weigted vertices represented as a list of tuples
    weights = [(0, 5), (3, 2), (1, 3)]

    # Creating a Graph object based on the given edges and weights
    myfloor = Graph(edges, weights)
    print(myfloor)

    print(myfloor.get_shortest_path(1,3))
    print(myfloor)