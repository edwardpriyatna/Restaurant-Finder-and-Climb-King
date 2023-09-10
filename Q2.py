import heapq


class Vertex:
    def __init__(self, name):
        self.name = name
        self.edges = []

    def add_edge(self, edge):
        self.edges.append(edge)


class Edge:
    def __init__(self, vertex, weight):
        self.vertex = vertex
        self.weight = weight


class Graph:
    def __init__(self, paths):
        self.vertices = {}
        for path in paths:
            self.add_path(path)

    def add_path(self, path):
        from_vertex = self.get_vertex(path[0])
        if from_vertex is None:
            from_vertex = Vertex(path[0])
            self.vertices[path[0]] = from_vertex
        to_vertex = self.get_vertex(path[1])
        if to_vertex is None:
            to_vertex = Vertex(path[1])
            self.vertices[path[1]] = to_vertex
        weight = path[2]
        edge = Edge(to_vertex, weight)
        from_vertex.add_edge(edge)

    def get_vertex(self, name):
        return self.vertices.get(name)

    def update_distance(self, current_vertex, edge, distances, previous_vertices):
        new_distance = distances[current_vertex] + edge.weight
        if new_distance < distances[edge.vertex]:
            distances[edge.vertex] = new_distance
            previous_vertices[edge.vertex] = current_vertex

    def update_distances(self, current_vertex, distances, previous_vertices):
        for edge in current_vertex.edges:
            self.update_distance(current_vertex, edge, distances, previous_vertices)

    def construct_path(self, start_name, exits, distances, previous_vertices):
        path = []
        exit_distances = [distances[self.get_vertex(exit)] for exit in exits]

        # If all exit vertices are unreachable from the start vertex
        if all(distance == float('inf') for distance in exit_distances):
            return (float('inf'), [])

        current_vertex = self.get_vertex(exits[exit_distances.index(min(exit_distances))])

        while previous_vertices[current_vertex] is not None:
            path.append(current_vertex.name)
            current_vertex = previous_vertices[current_vertex]

        if path:
            path.append(start_name)

        return (min(exit_distances), list(reversed(path)))

    def shortest_path_to_exit(self, start_name, exits):
        start_vertex = self.get_vertex(start_name)
        distances = {vertex: float('inf') for vertex in self.vertices.values()}
        previous_vertices = {vertex: None for vertex in self.vertices.values()}
        distances[start_vertex] = 0
        vertices = [(0, start_vertex)]

        while vertices:
            current_distance, current_vertex = heapq.heappop(vertices)
            if current_distance > distances[current_vertex]:
                continue
            self.update_distances(current_vertex, distances, previous_vertices)
            for edge in current_vertex.edges:
                if distances[edge.vertex] > distances[current_vertex] + edge.weight:
                    heapq.heappush(vertices, (distances[current_vertex] + edge.weight, edge.vertex))

        return self.construct_path(start_name, exits, distances, previous_vertices)

if __name__ == "__main__":
    # The paths represented as a list of tuples
    paths = [(0, 1, 4), (1, 2, 2), (2, 3, 3), (3, 4, 1), (1, 5, 2),
             (5, 6, 5), (6, 3, 2), (6, 4, 3), (1, 7, 4), (7, 8, 2),
             (8, 7, 2), (7, 3, 2), (8, 0, 11), (4, 3, 1), (4, 8, 10)]

    # Creating a Graph object based on the given paths
    myfloor = Graph(paths)

    # Test the shortest_path_to_exit method
    print(myfloor.shortest_path_to_exit(5, [7]))
