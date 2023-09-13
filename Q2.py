import heapq
class Location:
    def __init__(self, location_id):
        self.id = location_id
        self.paths = []  # List of Path objects
        self.key = None  # Key object if a key is present
        self.visited = False
        self.discovered = False
        self.time_to_reach = float('inf')  # Initialize with infinity

    def __str__(self):
        path_info = ", ".join([f"({path.destination}, Time: {path.time})" for path in self.paths])
        if self.key:
            key_info = f"Key at Location: {self.key.location_id} (Time to Pickup: {self.key.time_to_pickup})"
        else:
            key_info = "No Key"
        return f"Location {self.id} - Paths: [{path_info}], {key_info}, Visited: {self.visited}, Discovered: {self.discovered}, Time to Reach: {self.time_to_reach}"

class Path:
    def __init__(self, source, destination, time):
        self.source = source
        self.destination = destination
        self.time = time

    def __str__(self):
        return f"Path from {self.source} to {self.destination} (Time: {self.time})"

class Key:
    def __init__(self, location_id, time_to_pickup):
        self.location_id = location_id
        self.time_to_pickup = time_to_pickup

    def __str__(self):
        return f"Key at Location {self.location_id} (Time to Pickup: {self.time_to_pickup})"


class FloorGraph:
    def __init__(self, paths, keys):
        self.locations = []  # List of Location objects
        self.exits = []  # List of exit location IDs
        self.start = None  # Start location object
        self.construct_graph(paths, keys)

    def construct_graph(self, paths, keys):
        # Collect unique location IDs from paths and keys
        unique_location_ids = set()
        for u, v, _ in paths:
            unique_location_ids.add(u)
            unique_location_ids.add(v)
        for k, _ in keys:
            unique_location_ids.add(k)

        # Initialize Location objects
        for location_id in unique_location_ids:
            self.locations.append(Location(location_id))

        # Add paths to Location objects
        for u, v, x in paths:
            self.locations[u].paths.append(Path(u, v, x))

        # Add keys to Location objects
        for k, y in keys:
            self.locations[k].key = Key(k, y)

    def __str__(self):
        return "\n".join([str(location) for location in self.locations])

    def run_dijkstra_original(self, start):
        # Initialize priority queue (heap) for Dijkstra's algorithm
        priority_queue = [(0, start)]
        heapq.heapify(priority_queue)

        # Initialize the start location's time to reach as 0
        self.locations[start].time_to_reach = 0

        while priority_queue:
            # Get the location with the minimum time_to_reach value
            current_time, current_location = heapq.heappop(priority_queue)

            # If the current_time is greater than the recorded time_to_reach, skip
            if current_time > self.locations[current_location].time_to_reach:
                continue

            # Iterate through paths from the current location
            for path in self.locations[current_location].paths:
                next_location = path.destination
                next_time = current_time + path.time

                # If the new time is shorter, update the time_to_reach for the next_location
                if next_time < self.locations[next_location].time_to_reach:
                    self.locations[next_location].time_to_reach = next_time
                    # Add the next_location to the priority queue
                    heapq.heappush(priority_queue, (next_time, next_location))

    def reset_time_to_reach(self):
        # Reset time_to_reach to infinity for all locations except the start
        for location in self.locations:
            if location != self.start:
                location.time_to_reach = float('inf')

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
    myfloor.run_dijkstra_original(1)
    print('after')
    print(myfloor)


