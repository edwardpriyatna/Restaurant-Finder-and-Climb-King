from typing import List, Tuple, Optional
import heapq

class Location:
    def __init__(self, id: int, monster_defeat_time: int = 0, has_key: bool = False):
        self.id = id
        self.monster_defeat_time = monster_defeat_time
        self.paths = []
        self.has_key = has_key
        self.visited = False
        self.discovered = False

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

    def __str__(self):
        locations_str = '\n'.join([str(location) for location in self.locations])
        return f"FloorMap:\n{locations_str}"

    def _sort_exits(self, exits):
        return sorted(exits)

    def _binary_search(self, exits, target):
        left, right = 0, len(exits) - 1
        while left <= right:
            mid = left + (right - left) // 2
            if exits[mid] == target:
                return mid
            elif exits[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

    def climb(self, start, exits):
        exits = self._sort_exits(exits)
        min_heap = [(0, start, False, [])]  # (total_time, current_location, found_key, path)

        while min_heap:
            total_time, current_location, found_key, path = heapq.heappop(min_heap)

            if self.locations[current_location].visited:
                continue

            self.locations[current_location].visited = True
            path.append(current_location)

            if current_location in exits and found_key:
                exit_index = self._binary_search(exits, current_location)
                if exit_index != -1:
                    return total_time, path  # Found an exit with a key

            for path_obj in self.locations[current_location].paths:
                next_location = path_obj.end_location
                travel_time = path_obj.travel_time

                if not found_key and next_location.has_key and not next_location.discovered:
                    # Collecting the key is optional, so we explore both options
                    heapq.heappush(min_heap, (total_time + travel_time, next_location.id, True, list(path)))

                if not next_location.visited:
                    heapq.heappush(min_heap, (total_time + travel_time, next_location.id, found_key, list(path)))
                    next_location.discovered = True

        return None  # No valid route found




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




