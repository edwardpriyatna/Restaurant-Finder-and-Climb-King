import heapq


class Vertex:
    def __init__(self, id, weight=0):
        self.id = id
        self.weight = weight
        self.edges = None
        self.next = None
        self.visited = False
        self.discovered = False

    def add_edge(self, edge):
        if not self.edges:
            self.edges = edge
        else:
            current_edge = self.edges
            while current_edge.next:
                current_edge = current_edge.next
            current_edge.next = edge


class Edge:
    def __init__(self, start_vertex, end_vertex, weight):
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex
        self.weight = weight
        self.next = None


class Graph:
    def __init__(self, paths, keys):
        self.vertices = Vertex(0)
        current_vertex = self.vertices
        for i in range(1, max(max(paths)) + 1):
            current_vertex.next = Vertex(i)
            current_vertex = current_vertex.next

        for key in keys:
            current_vertex = self.vertices
            while current_vertex and current_vertex.id != key[0]:
                current_vertex = current_vertex.next
            if current_vertex:
                current_vertex.weight = key[1]

        for path in paths:
            start_vertex = self.vertices
            while start_vertex and start_vertex.id != path[0]:
                start_vertex = start_vertex.next

            end_vertex = self.vertices
            while end_vertex and end_vertex.id != path[1]:
                end_vertex = end_vertex.next

            if start_vertex and end_vertex:
                edge = Edge(start_vertex, end_vertex, path[2])
                start_vertex.add_edge(edge)


def modified_dijkstra(graph, start_id, end_id):
    queue = []
    heapq.heappush(queue, (0, start_id, [], 0))

    start_node = graph.vertices
    while start_node and start_node.id != start_id:
        start_node = start_node.next

    if start_node:
        start_node.discovered = True

    while queue:
        (cost, node_id, path, added_weight) = heapq.heappop(queue)

        node_weight = 0
        node = graph.vertices
        while node and node.id != node_id:
            node = node.next

        if node and not node.visited:
            node.visited = True

            path = path + [node_id]

            if node.weight > 0 and added_weight == 0:
                node_weight = node.weight
                added_weight += node_weight

            if node_id == end_id and added_weight > 0:
                return cost + added_weight, path

            edge = None
            if node:
                edge = node.edges

            while edge:
                total_cost = cost + edge.weight + node_weight

                next_node = graph.vertices
                while next_node and next_node.id != edge.end_vertex.id:
                    next_node = next_node.next

                if next_node and not next_node.discovered:
                    next_node.discovered = True

                    heapq.heappush(queue, (total_cost, edge.end_vertex.id, path, added_weight))

                edge = edge.next

    return float("inf"), []


# Define your graph here. For example:
paths = [(0, 1, 4), (0, 3, 2), (0, 2, 3), (2, 3, 2), (3, 0, 3)]
keys = [(0, 5), (3, 2), (1, 3)]
graph = Graph(paths, keys)

print(modified_dijkstra(graph, 0, 3))