from typing import List, Tuple

class Path:
    def __init__(self, destination: int, travel_time: int):
        self.destination = destination
        self.travel_time = travel_time

    def __str__(self) -> str:
        return f'Path(destination={self.destination}, travel_time={self.travel_time})'

class Location:
    def __init__(self, location_id: int):
        self.location_id = location_id
        self.monster_defeat_time = 0
        self.paths: List[Path] = []

    def add_path(self, path: Path) -> None:
        self.paths.append(path)

    def add_key(self, monster_defeat_time: int) -> None:
        self.monster_defeat_time = monster_defeat_time

    def __str__(self) -> str:
        paths_str = ', '.join(str(path) for path in self.paths)
        return f'Location(location_id={self.location_id}, monster_defeat_time={self.monster_defeat_time}, paths=[{paths_str}])'

class FloorGraph:
    def __init__(self, paths_list: List[Tuple[int, int, int]], keys_list: List[Tuple[int, int]]):
        max_location_id = max(max(max(paths_list), max(keys_list)))
        self.total_locations = max_location_id + 1
        self.locations: List[Location] = [Location(i) for i in range(self.total_locations)]
        self.add_paths(paths_list)
        self.add_keys(keys_list)
        self.sort_locations()

    def add_paths(self, paths_list: List[Tuple[int, int, int]]) -> None:
        for path in paths_list:
            start_location, destination_location, travel_time = path
            path_obj = Path(destination_location, travel_time)
            self.locations[start_location].add_path(path_obj)

    def add_keys(self, keys_list: List[Tuple[int, int]]) -> None:
        for key in keys_list:
            location_id, monster_defeat_time = key
            self.locations[location_id].add_key(monster_defeat_time)

    def sort_locations(self) -> None:
        self.locations.sort(key=lambda location: location.location_id)

    def __str__(self) -> str:
        return '\n'.join(str(location) for location in self.locations)

if __name__ == "__main__":
    # The paths represented as a list of tuples
    paths = [(0, 1, 4), (0, 3, 2), (0, 2, 3), (2, 3, 2), (3, 0, 3)]
    # The keys represented as a list of tuples
    keys = [(0, 5), (3, 2), (1, 3)]
    # Creating a FloorGraph object based on the given paths and keys
    myfloor = FloorGraph(paths, keys)
    print(myfloor)
