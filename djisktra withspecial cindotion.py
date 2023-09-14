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

    def __lt__(self, other):
        return self.time_to_reach < other.time_to_reach

    def __str__(self):
        return f"Vertex {self.name}, weight {self.weight}, visited {self.visited}, discovered {self.discovered}, " \
               f"time_to_reach {self.time_to_reach}, edges {[str(edge) for edge in self.edges]}, " \
               f"previous_vertex {self.previous_vertex.name if self.previous_vertex else None}"

class Edge:
    def __init__(self, to_vertex, weight):
        self.to_vertex = to_vertex
        self.weight = weight

    def __str__(self):
        return f"Edge to {self.to_vertex.name}, weight {self.weight}"

class Graph:
    def __init__(self,edges,weights):
        self.vertices = []
        self.construct_graph(edges, weights)

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def add_edge(self, from_vertex_index, to_vertex_index, weight):
        edge_instance = Edge(self.vertices[to_vertex_index], weight)
        self.vertices[from_vertex_index].edges.append(edge_instance)

    def construct_graph(self, edges, weights):
        for i in range(max(max(edges, key=lambda x: max(x[:2]))[:2]) + 1):
            self.add_vertex(Vertex(i))

        for weight in weights:
            self.vertices[weight[0]].weight = weight[1]

        for edge in edges:
            self.add_edge(*edge)

    def dijkstra(self, start_vertex):
        queue = []
        start_vertex.time_to_reach = 0
        heapq.heappush(queue, start_vertex)

        while queue:
            current_vertex = heapq.heappop(queue)

            if current_vertex.visited:
                continue

            current_vertex.visited = True

            for edge in current_vertex.edges:
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

    def reset(self):
        for vertex in self.vertices:
            vertex.visited = False
            vertex.discovered = False
            vertex.time_to_reach = float('inf')
            vertex.previous_vertex = None

    def flip_graph(self):
        # Create a new list of vertices with the same names but no edges
        flipped_vertices = [Vertex(i) for i in range(len(self.vertices))]

        # Iterate over the original vertices and their edges
        for vertex in self.vertices:
            for edge in vertex.edges:
                # Add a new edge with reversed direction to the corresponding vertex in the new list
                flipped_edge = Edge(flipped_vertices[vertex.name], edge.weight)
                flipped_vertices[edge.to_vertex.name].edges.append(flipped_edge)

        # Replace the original list of vertices with the new one
        self.vertices = flipped_vertices

    def add_new_location(self, exits):
        # Create a new vertex and add it to the list of vertices
        new_vertex = Vertex(len(self.vertices))
        self.vertices.append(new_vertex)

        # Connect the new vertex to all exits with an edge of weight 0
        for exit in exits:
            exit_edge = Edge(self.vertices[exit], 0)
            new_vertex.edges.append(exit_edge)

    def get_minimum_weighted_vertice(self, start_vertex_index):
        start_vertex = self.vertices[start_vertex_index]
        self.dijkstra(start_vertex)

        min_weighted_vertex = None
        for vertex in self.vertices:
            if vertex.weight != 0 and (
                    min_weighted_vertex is None or vertex.time_to_reach + vertex.weight < min_weighted_vertex.time_to_reach + min_weighted_vertex.weight):
                min_weighted_vertex = vertex

        if min_weighted_vertex is None:
            return None

        path = []
        current_vertex = min_weighted_vertex

        while current_vertex is not None:
            path.append(current_vertex.name)
            current_vertex = current_vertex.previous_vertex

        path.reverse()
        return min_weighted_vertex.name, min_weighted_vertex.time_to_reach, path, min_weighted_vertex.weight

    def get_shortest_path_all_weighted_vertices(self, start_vertex_index):
        start_vertex = self.vertices[start_vertex_index]
        self.dijkstra(start_vertex)

        shortest_paths = []
        for vertex in self.vertices:
            if vertex.weight != 0 and vertex.time_to_reach != float('inf'):
                path = []
                current_vertex = vertex

                while current_vertex is not None:
                    path.append(current_vertex.name)
                    current_vertex = current_vertex.previous_vertex

                path.reverse()
                shortest_paths.append((vertex.time_to_reach, path, vertex.weight))

        return shortest_paths
    def __str__(self):
        return "\n".join(str(vertex) for vertex in self.vertices)

if __name__ == "__main__":
    # Example 1
    # The paths represented as a list of tuples
    paths = [(0, 1, 4), (1, 2, 2), (2, 3, 3), (3, 4, 1), (1, 5, 2),
             (5, 6, 5), (6, 3, 2), (6, 4, 3), (1, 7, 4), (7, 8, 2),
             (8, 7, 2), (7, 3, 2), (8, 0, 11), (4, 3, 1), (4, 8, 10)]
    # The keys represented as a list of tuples
    keys = [(5, 10), (6, 1), (7, 5), (0, 3), (8, 4)]
    # Creating a FloorGraph object based on the given paths
    myfloor = Graph(paths, keys)
    print(myfloor.get_shortest_path_all_weighted_vertices(1))
