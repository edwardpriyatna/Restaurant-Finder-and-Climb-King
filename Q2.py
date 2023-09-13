from typing import List, Tuple, Optional
import heapq

class Location:
    def __init__(self, id: int, monster_defeat_time: int = 0, has_key: bool = False):
        self.id = id
        self.monster_defeat_time = monster_defeat_time
        self.paths = []
        self.has_key = has_key

    def add_path(self, destination, travel_time):
        self.paths.append(Path(self, destination, travel_time))

    def __str__(self):
        paths_str = ', '.join([str(path) for path in self.paths])
        return f"Location(id={self.id}, monster_defeat_time={self.monster_defeat_time}, has_key={self.has_key}, paths=[{paths_str}])"

class Path:
    def __init__(self, start_location: Location, end_location: Location, travel_time: int):
        self.start_location = start_location
        self.end_location = end_location
        self.travel_time = travel_time

    def __str__(self):
        return f"Path(end_location={self.end_location.id}, travel_time={self.travel_time})"

class FloorGraph:
    def __init__(self, paths, keys):
        self.total_locations = self._get_total_locations(paths)
        self.locations = [Location(i) for i in range(self.total_locations)]
        self._populate_locations_with_paths(paths)
        self._populate_locations_with_keys(keys)

    def _get_total_locations(self, paths):
        return max(max(paths, key=lambda x: max(x[0], x[1]))[:2]) + 1

    def _populate_locations_with_paths(self, paths):
        for path in paths:
            start_location_id, end_location_id, travel_time = path
            path = Path(self.locations[start_location_id], self.locations[end_location_id], travel_time)
            self.locations[start_location_id].add_path(self.locations[end_location_id], travel_time)

    def _populate_locations_with_keys(self, keys):
        for key in keys:
            key_location_id, monster_defeat_time = key
            self.locations[key_location_id].has_key = True
            self.locations[key_location_id].monster_defeat_time = monster_defeat_time

    def climb(self, start, exits):
        exit_locations = set(exits)
        min_heap = [(0, start, set(), [start])]  # (total_time, current_location, collected_keys, path)

        while min_heap:
            total_time, current_location, collected_keys, path = heapq.heappop(min_heap)

            if current_location in exit_locations:
                return total_time, path

            for path_obj in self.locations[current_location].paths:
                next_location = path_obj.end_location
                travel_time = path_obj.travel_time

                if next_location.id not in collected_keys:
                    next_keys = set(collected_keys)
                    if next_location.has_key:
                        next_keys.add(next_location.id)
                        heapq.heappush(min_heap, (total_time + travel_time + next_location.monster_defeat_time, next_location.id, next_keys, path + [next_location.id]))
                    else:
                        heapq.heappush(min_heap, (total_time + travel_time, next_location.id, next_keys, path + [next_location.id]))

        return None  # No valid route found

if __name__ == "__main__":
    # Create a FloorGraph object and perform the climb operation
    paths = [(0, 1, 4), (1, 2, 2), (2, 3, 3), (3, 4, 1), (1, 5, 2), (5, 6, 5), (6, 3, 2), (6, 4, 3), (1, 7, 4), (7, 8, 2), (8, 7, 2), (7, 3, 2), (8, 0, 11), (4, 3, 1), (4, 8, 10)]
    keys = [(5, 10), (6, 1), (7, 5), (0, 3), (8, 4)]
    myfloor = FloorGraph(paths, keys)

    start = 1
    exits = [7, 2, 4]
    result = myfloor.climb(start, exits)
    if result:
        total_time, path = result
        print(f"Total Time: {total_time}")
        print(f"Path: {path}")
    else:
        print("No valid route found")

if __name__ == "__main__":
    # The paths represented as a list of tuples
    paths = [(0, 1, 4), (1, 2, 2), (2, 3, 3), (3, 4, 1), (1, 5, 2),
             (5, 6, 5), (6, 3, 2), (6, 4, 3), (1, 7, 4), (7, 8, 2),
             (8, 7, 2), (7, 3, 2), (8, 0, 11), (4, 3, 1), (4, 8, 10)]
    # The keys represented as a list of tuples
    keys = [(5, 10), (6, 1), (7, 5), (0, 3), (8, 4)]
    # Creating a FloorGraph object based on the given paths
    myfloor = FloorGraph(paths, keys)
    print(myfloor)
    start = 1
    exits = [7, 2, 4]
    print(myfloor.climb(start, exits))




