from typing import List, Tuple, Optional
import heapq
class Location:
    def __init__(self, id: int, monster_defeat_time: int = 0):
        self.id = id
        self.monster_defeat_time = monster_defeat_time
        self.paths = []

    def __str__(self):
        paths_str = ', '.join([str(path) for path in self.paths])
        return f"Location(id={self.id}, monster_defeat_time={self.monster_defeat_time}, paths=[{paths_str}])"

class Path:
    def __init__(self, start_location: Location, end_location: Location, travel_time: int):
        self.start_location = start_location
        self.end_location = end_location
        self.travel_time = travel_time

    def __str__(self):
        return f"Path(end_location={self.end_location.id}, travel_time={self.travel_time})"

class FloorGraph:
    def __init__(self, paths: List[Tuple[int, int, int]], keys: List[Tuple[int, int]]):
        self.total_locations = self._get_total_locations(paths)
        self.locations = [Location(i) for i in range(self.total_locations)]
        self._populate_locations_with_paths(paths)
        self._populate_locations_with_keys(keys)

    def _get_total_locations(self, paths: List[Tuple[int, int, int]]) -> int:
        return max(max(paths, key=lambda x: max(x[0], x[1]))[:2]) + 1

    def _populate_locations_with_paths(self, paths: List[Tuple[int, int, int]]) -> None:
        for path in paths:
            start_location_id, end_location_id, travel_time = path
            path = Path(self.locations[start_location_id], self.locations[end_location_id], travel_time)
            self.locations[start_location_id].paths.append(path)

    def _populate_locations_with_keys(self, keys: List[Tuple[int, int]]) -> None:
        for key in keys:
            key_location_id, monster_defeat_time = key
            self.locations[key_location_id].monster_defeat_time = monster_defeat_time

    def __str__(self):
        locations_str = '\n'.join([str(location) for location in self.locations])
        return f"FloorMap:\n{locations_str}"


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


