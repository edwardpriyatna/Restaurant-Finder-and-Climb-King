import heapq
from typing import List, Optional

class Location:
    def __init__(self, ID):
        self.ID = ID
        self.visited = False
        self.discovered = False
        self.time_to_reach = float('inf')
        self.paths = []
        self.previous_location = None

    def __lt__(self, other) -> bool:
        return self.time_to_reach < other.time_to_reach

    def __str__(self) -> str:
        return f"Vertex {self.ID}, visited {self.visited}, discovered {self.discovered}, " \
               f"time_to_reach {self.time_to_reach}, edges {[str(path) for path in self.paths]}, " \
               f"previous_vertex {self.previous_location.ID if self.previous_location else None}"

class Path:
    def __init__(self, v, x):
        self.v = v
        self.x = x

    def __str__(self) -> str:
        return f"Edge to {self.v.ID}, weight {self.x}"

class Key:
    def __init__(self, k, y):
        self.k = k
        self.time_to_reach_key = 0
        self.y = y

    def __str__(self) -> str:
        return f"Weight of vertex {self.k} with distance to reach {self.time_to_reach_key} " \
               f"and distance to get {self.y}"

class FloorGraph:
    def __init__(self, paths: List[List[int]], keys: List[List[int]]):
        self.locations = []
        self.keys = []
        self.construct_graph(paths, keys)

    def add_location(self, location):
        self.locations.append(location)

    def add_key(self, key):
        self.keys.append(key)

    def add_path(self, from_k: int, v_index: int, x: int):
        path_instance = Path(self.locations[v_index], x)
        self.locations[from_k].paths.append(path_instance)

    def construct_graph(self, paths: List[List[int]], keys: List[List[int]]):
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
                tentative_distance = current_location.time_to_reach + path.x
                if tentative_distance < path.v.time_to_reach:
                    path.v.time_to_reach = tentative_distance
                    path.v.discovered = True
                    path.v.previous_location = current_location
                    heapq.heappush(queue, path.v)

    def get_shortest_path(self, start_k: int, end_k: int) -> Optional[List[int]]:
        start_location = self.locations[start_k]
        end_location = self.locations[end_k]
        self.dijkstra(start_location)

        if end_location.time_to_reach == float('inf'):
            return None

        path = []
        current_location = end_location

        while current_location is not None:
            path.insert(0, current_location.ID)
            current_location = current_location.previous_location

        return path

    def reset(self):
        for location in self.locations:
            location.visited = False
            location.discovered = False
            location.time_to_reach = float('inf')
            location.previous_location = None

    def flip_graph(self):
        flipped_locations = [Location(i) for i in range(len(self.locations))]

        for location in self.locations:
            for path in location.paths:
                flipped_path = Path(flipped_locations[location.ID], path.x)
                flipped_locations[path.v.ID].paths.append(flipped_path)

        self.locations = flipped_locations

    def add_new_location(self, exits: List[int]):
        new_location = Location(len(self.locations))
        self.locations.append(new_location)

        for exit_location in exits:
            exit_path = Path(self.locations[exit_location], 0)
            new_location.paths.append(exit_path)

    def get_minimum_distance_to_key(self, start: int):
        self.dijkstra(self.locations[start])

        for key in self.keys:
            location = self.locations[key.k]
            key.time_to_reach_key += location.time_to_reach

    def get_minimum_key(self) -> 'Key':
        return min(self.keys, key=lambda key: key.time_to_reach_key + key.y)

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
        route_part1 = self.get_shortest_path(start, location_to_grab_key.k)
        if route_part1 is None:
            return None
        route_part1.pop() #pop the location where the key is grabbed

        self.reset()
        route_part2 = self.get_shortest_path(location_to_grab_key.k, len(self.locations) - 1)
        route_part2.pop() #pop the new location
        total_time= location_to_grab_key.time_to_reach_key + location_to_grab_key.y
        route=route_part1 + route_part2

        self.reset_keys()
        self.reset()
        self.delete_new_location()
        return total_time,route

    def reset_keys(self):
        for key in self.keys:
            key.time_to_reach = 0

    def delete_new_location(self):
        new_location = self.locations.pop()

        for location in self.locations:
            location.paths = [path for path in location.paths if path.v != new_location]

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