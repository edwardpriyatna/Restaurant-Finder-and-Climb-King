import heapq
from typing import List, Optional

class Location:
    def __init__(self, name):
        self.name = name
        self.visited = False
        self.discovered = False
        self.time_to_reach = float('inf')
        self.paths = []
        self.previous_location = None

    def __lt__(self, other):
        return self.time_to_reach < other.time_to_reach

    def __str__(self):
        return f"Vertex {self.name}, visited {self.visited}, discovered {self.discovered}, " \
               f"time_to_reach {self.time_to_reach}, edges {[str(path) for path in self.paths]}, " \
               f"previous_vertex {self.previous_location.name if self.previous_location else None}"

class Path:
    def __init__(self, to_location, travel_time):
        self.to_location = to_location
        self.travel_time = travel_time

    def __str__(self):
        return f"Edge to {self.to_location.name}, weight {self.travel_time}"

class Key:
    def __init__(self, location_index, time_to_fight):
        self.location_index = location_index
        self.time_to_reach_key = 0
        self.time_to_fight = time_to_fight

    def __str__(self):
        return f"Weight of vertex {self.location_index} with distance to reach {self.time_to_reach_key} " \
               f"and distance to get {self.time_to_fight}"

class FloorGraph:
    def __init__(self, paths, keys):
        self.locations = []
        self.keys = []
        self.construct_graph(paths, keys)

    def add_location(self, location):
        self.locations.append(location)

    def add_key(self, key):
        self.keys.append(key)

    def add_path(self, from_location_index, to_location_index, travel_time):
        path_instance = Path(self.locations[to_location_index], travel_time)
        self.locations[from_location_index].paths.append(path_instance)

    def construct_graph(self, paths, keys):
        for i in range(max(max(paths, key=lambda x: max(x[:2]))[:2]) + 1):
            self.add_location(Location(i))

        for key in keys:
            self.add_key(Key(key[0], key[1]))

        for path in paths:
            self.add_path(*path)

    def dijkstra(self, start_location):
        queue = []
        start_location.time_to_reach = 0
        heapq.heappush(queue, start_location)

        while queue:
            current_location = heapq.heappop(queue)

            if current_location.visited:
                continue

            current_location.visited = True

            for path in current_location.paths:
                tentative_distance = current_location.time_to_reach + path.travel_time
                if tentative_distance < path.to_location.time_to_reach:
                    path.to_location.time_to_reach = tentative_distance
                    path.to_location.discovered = True
                    path.to_location.previous_location = current_location
                    heapq.heappush(queue, path.to_location)

    def get_shortest_path(self, start_location_index, end_location_index):
        start_location = self.locations[start_location_index]
        end_location = self.locations[end_location_index]
        self.dijkstra(start_location)

        if end_location.time_to_reach == float('inf'):
            return None

        path = []
        current_location = end_location

        while current_location is not None:
            path.insert(0, current_location.name)
            current_location = current_location.previous_location

        return path

    def reset(self):
        for location in self.locations:
            location.visited = False
            location.discovered = False
            location.time_to_reach = float('inf')
            location.previous_location = None

    import heapq
    from typing import List, Optional

    class Location:
        def __init__(self, name: int):
            self.name: int = name
            self.visited: bool = False
            self.discovered: bool = False
            self.time_to_reach: float = float('inf')
            self.paths: List['Path'] = []
            self.previous_location: Optional['Location'] = None

        def __lt__(self, other: 'Location') -> bool:
            return self.time_to_reach < other.time_to_reach

        def __str__(self) -> str:
            return f"Vertex {self.name}, visited {self.visited}, discovered {self.discovered}, " \
                   f"time_to_reach {self.time_to_reach}, edges {[str(path) for path in self.paths]}, " \
                   f"previous_vertex {self.previous_location.name if self.previous_location else None}"

    class Path:
        def __init__(self, to_location: 'Location', travel_time: int):
            self.to_location: 'Location' = to_location
            self.travel_time: int = travel_time

        def __str__(self) -> str:
            return f"Edge to {self.to_location.name}, weight {self.travel_time}"

    class Key:
        def __init__(self, location_index: int, time_to_fight: int):
            self.location_index: int = location_index
            self.time_to_reach_key: int = 0
            self.time_to_fight: int = time_to_fight

        def __str__(self) -> str:
            return f"Weight of vertex {self.location_index} with distance to reach {self.time_to_reach_key} " \
                   f"and distance to get {self.time_to_fight}"

    class FloorGraph:
        def __init__(self, paths: List[List[int]], keys: List[List[int]]):
            self.locations: List['Location'] = []
            self.keys: List['Key'] = []
            self.construct_graph(paths, keys)

        def add_location(self, location: 'Location'):
            self.locations.append(location)

        def add_key(self, key: 'Key'):
            self.keys.append(key)

        def add_path(self, from_location_index: int, to_location_index: int, travel_time: int):
            path_instance = Path(self.locations[to_location_index], travel_time)
            self.locations[from_location_index].paths.append(path_instance)

        def construct_graph(self, paths: List[List[int]], keys: List[List[int]]):
            for i in range(max(max(paths, key=lambda x: max(x[:2]))[:2]) + 1):
                self.add_location(Location(i))

            for key in keys:
                self.add_key(Key(key[0], key[1]))

            for path in paths:
                self.add_path(*path)

        def dijkstra(self, start_location: 'Location'):
            queue = []
            start_location.time_to_reach = 0
            heapq.heappush(queue, start_location)

            while queue:
                current_location = heapq.heappop(queue)

                if current_location.visited:
                    continue

                current_location.visited = True

                for path in current_location.paths:
                    tentative_distance = current_location.time_to_reach + path.travel_time
                    if tentative_distance < path.to_location.time_to_reach:
                        path.to_location.time_to_reach = tentative_distance
                        path.to_location.discovered = True
                        path.to_location.previous_location = current_location
                        heapq.heappush(queue, path.to_location)

        def get_shortest_path(self, start_location_index: int, end_location_index: int) -> Optional[List[int]]:
            start_location = self.locations[start_location_index]
            end_location = self.locations[end_location_index]
            self.dijkstra(start_location)

            if end_location.time_to_reach == float('inf'):
                return None

            path = []
            current_location = end_location

            while current_location is not None:
                path.insert(0, current_location.name)
                current_location = current_location.previous_location

            return path

        def reset(self):
            for location in self.locations:
                location.visited = False
                location.discovered = False
                location.time_to_reach = float('inf')
                location.previous_location = None

    def flip_graph(self):
        # Create a new list of vertices with the same names but no edges
        flipped_locations: List['Location'] = [Location(i) for i in range(len(self.locations))]

        # Iterate over the original vertices and their edges
        for location in self.locations:
            for path in location.paths:
                # Add a new edge with reversed direction to the corresponding vertex in the new list
                flipped_path: 'Path' = Path(flipped_locations[location.name], path.travel_time)
                flipped_locations[path.to_location.name].paths.append(flipped_path)

        # Replace the original list of vertices with the new one
        self.locations = flipped_locations

    def add_new_location(self, exits: List[int]):
        # Create a new vertex and add it to the list of vertices
        new_location: 'Location' = Location(len(self.locations))
        self.locations.append(new_location)

        # Connect the new vertex to all exits with an edge of weight 0
        for exit_location in exits:
            exit_path: 'Path' = Path(self.locations[exit_location], 0)
            new_location.paths.append(exit_path)

    def get_minimum_distance_to_key(self, start: int):
        # Run Dijkstra's algorithm from the start vertex
        self.dijkstra(self.locations[start])

        # Update the distance_to_reach of each weight
        for key in self.keys:
            location: 'Location' = self.locations[key.location_index]
            key.time_to_reach_key += location.time_to_reach

    def get_minimum_key(self) -> 'Key':
        return min(self.keys, key=lambda key: key.time_to_reach_key + key.time_to_fight)

    def find_location_to_grab_key(self, start: int, exits: List[int]) -> 'Key':
        self.get_minimum_distance_to_key(start)
        self.reset()
        self.flip_graph()
        self.add_new_location(exits)
        self.get_minimum_distance_to_key(len(self.locations) - 1)
        self.flip_graph()
        self.reset()
        return self.get_minimum_key()

    def climb(self, start: int, exits: List[int]) -> Optional[tuple]:
        location_to_grab_key = self.find_location_to_grab_key(start, exits)
        sequence_part1 = self.get_shortest_path(start, location_to_grab_key.location_index)
        if sequence_part1 is None:
            return None
        sequence_part1.pop()
        self.reset()

        sequence_part2 = self.get_shortest_path(location_to_grab_key.location_index, len(self.locations) - 1)
        sequence_part2.pop()
        return_tuple = (location_to_grab_key.time_to_reach_key + location_to_grab_key.time_to_fight, sequence_part1 + sequence_part2)

        self.reset_keys()
        self.reset()
        self.delete_new_location()
        return return_tuple

    def reset_keys(self):
        for key in self.keys:
            key.time_to_reach = 0

    def delete_new_location(self):
        # Remove the last vertex from the list of vertices
        new_location: 'Location' = self.locations.pop()

        # Iterate over all vertices and remove any edge that connects to the new location
        for location in self.locations:
            location.paths = [path for path in location.paths if path.to_location != new_location]

    def __str__(self) -> str:
        return "\n".join(str(location) for location in self.locations)


if __name__ == "__main__":
    # Example 1
    # The paths represented as a list of tuples
    paths = [(0, 1, 4), (1, 2, 2), (2, 3, 3), (3, 4, 1), (1, 5, 2),
             (5, 6, 5), (6, 3, 2), (6, 4, 3), (1, 7, 4), (7, 8, 2),
             (8, 7, 2), (7, 3, 2), (8, 0, 11), (4, 3, 1), (4, 8, 10)]
    # The keys represented as a list of tuples
    keys = [(5, 10), (6, 1), (7, 5), (0, 3), (8, 4)]
    # Creating a FloorGraph object based on the given paths
    myfloor = FloorGraph(paths, keys)
    start = 3
    exits = [4]
    print(myfloor.climb(start,exits))