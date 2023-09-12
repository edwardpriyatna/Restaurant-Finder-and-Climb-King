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

    def climb(self, start: int, exits: List[int]) -> Optional[Tuple[int, List[int]]]:
        # Initialize the priority queue with the start location
        queue = [(0, start, [])]

        # Initialize a list to keep track of the shortest time to reach each location
        shortest_times = [float('inf')] * self.total_locations
        shortest_times[start] = 0

        # While there are locations to visit
        while queue:
            # Get the location with the shortest travel time so far
            time_so_far, current_location_id, route_so_far = heapq.heappop(queue)

            # If this location has a key and it's one of the exits
            if self.locations[current_location_id].monster_defeat_time > 0 and current_location_id in exits:
                # Return the total time and the route including this location
                return time_so_far + self.locations[current_location_id].monster_defeat_time, route_so_far + [
                    current_location_id]

            # If this is a new shortest time to this location
            if time_so_far < shortest_times[current_location_id]:
                # Update the shortest time to this location
                shortest_times[current_location_id] = time_so_far

                # For each path from this location
                for path in self.locations[current_location_id].paths:
                    # Add the location at the end of the path to the queue with the updated total time and route
                    heapq.heappush(queue, (time_so_far + path.travel_time + (self.locations[
                                                                                 path.end_location.id].monster_defeat_time if path.end_location.id != current_location_id else 0),
                                           path.end_location.id,
                                           route_so_far + [current_location_id]))

        # If no route was found that includes defeating a monster and reaching an exit
        return None

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
    print(myfloor.climb(start,exits))

