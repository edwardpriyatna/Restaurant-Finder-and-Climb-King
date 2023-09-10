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
        self.vertices = []
        for path in paths:
            self.add_path(path)

    def add_path(self, path):
        from_vertex = self.get_vertex(path[0])
        if from_vertex is None:
            from_vertex = Vertex(path[0])
            self.vertices.append(from_vertex)
        to_vertex = self.get_vertex(path[1])
        if to_vertex is None:
            to_vertex = Vertex(path[1])
            self.vertices.append(to_vertex)
        weight = path[2]
        edge = Edge(to_vertex, weight)
        from_vertex.add_edge(edge)

    def get_vertex(self, name):
        for vertex in self.vertices:
            if vertex.name == name:
                return vertex
        return None

    def update_distance(self, current_vertex, edge, distances, previous_vertices):
        new_distance = distances[self.vertices.index(current_vertex)] + edge.weight
        if new_distance < distances[self.vertices.index(edge.vertex)]:
            distances[self.vertices.index(edge.vertex)] = new_distance
            previous_vertices[self.vertices.index(edge.vertex)] = current_vertex

    def update_distances(self, current_vertex, distances, previous_vertices):
        for edge in current_vertex.edges:
            self.update_distance(current_vertex, edge, distances, previous_vertices)

    def construct_path(self, start_name, exits, distances, previous_vertices):
        path = []
        exit_distances = [distances[self.vertices.index(self.get_vertex(exit))] for exit in exits]
        current_vertex = self.get_vertex(exits[exit_distances.index(min(exit_distances))])

        while previous_vertices[self.vertices.index(current_vertex)] is not None:
            path.append(current_vertex.name)
            current_vertex = previous_vertices[self.vertices.index(current_vertex)]

        if path:
            path.append(start_name)

        return (min(exit_distances), list(reversed(path)))

    def shortest_path_to_exit(self, start_name, exits):
        start_vertex = self.get_vertex(start_name)
        distances = [float('inf')] * len(self.vertices)
        previous_vertices = [None] * len(self.vertices)
        distances[self.vertices.index(start_vertex)] = 0
        vertices = [(0, start_vertex)]

        while vertices:
            current_distance, current_vertex = heapq.heappop(vertices)
            if current_distance > distances[self.vertices.index(current_vertex)]:
                continue
            self.update_distances(current_vertex, distances, previous_vertices)
            for edge in current_vertex.edges:
                if distances[self.vertices.index(edge.vertex)] > distances[
                    self.vertices.index(current_vertex)] + edge.weight:
                    heapq.heappush(vertices,
                                   (distances[self.vertices.index(current_vertex)] + edge.weight, edge.vertex))

        return self.construct_path(start_name, exits, distances, previous_vertices)

if __name__ == "__main__":
    # The paths represented as a list of tuples
    paths = [(0, 1, 4), (0, 3, 2), (0, 2, 3), (2, 3, 2), (3, 0, 3)]

    # Creating a Graph object based on the given paths
    myfloor = Graph(paths)

    # Test the shortest_path_to_exit method
    print(myfloor.shortest_path_to_exit(0, [1]))
