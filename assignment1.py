from typing import List, Tuple, Optional
import heapq
def restaurantFinder(d: int, site_list: List[int]) -> Tuple[int, List[int]]:
    """
    Function description:
    This function helps a fast food chain to choose the sites to open restaurants such that no two restaurants are
    within a certain distance of each other and the overall revenue is maximised.

    Approach description:
    The function uses dynamic programming to solve this problem. It maintains an array `max_revenue` to store the maximum
    revenue that can be obtained for each site, and an array `chosen_sites` to store the chosen sites that contribute to the
    maximum revenue.

    :Input:
    d: The minimum distance between any two chosen sites.
    site_list: A list of revenues for each site.

    :Output, return or postcondition:
    The function returns a tuple with two elements:
    - The maximum total revenue that can be obtained.
    - A list of the chosen sites (1-indexed).

    :Time complexity:
    The time complexity of the function is O(N), where N is the number of potential sites.

    :Aux space complexity:
    The auxiliary space complexity of the function is also O(N).
    """
    N = len(site_list)
    total_revenue = [0]*N
    selected_sites = [0]*N

    # Initialize base cases
    total_revenue[0] = site_list[0] if site_list[0] > 0 else 0
    selected_sites[0] = [0] if site_list[0] > 0 else []

    for i in range(1, N):
        # If no restaurant within d km, consider the current site
        if i < d:
            if site_list[i] > total_revenue[i-1]:
                total_revenue[i] = site_list[i]
                selected_sites[i] = [i]
            else:
                total_revenue[i] = total_revenue[i-1]
                selected_sites[i] = selected_sites[i-1].copy()
        else:
            # Consider the current site and the maximum revenue from sites that are at least d km away
            include_site = site_list[i] + (total_revenue[i-d-1] if i-d-1 >= 0 else 0)
            exclude_site = total_revenue[i-1]

            if include_site > exclude_site:
                total_revenue[i] = include_site
                if i-d-1 >= 0:
                    selected_sites[i] = selected_sites[i-d-1].copy()
                else:
                    selected_sites[i] = []
                selected_sites[i].append(i)
            else:
                total_revenue[i] = exclude_site
                selected_sites[i] = selected_sites[i-1].copy()

    return (total_revenue[-1], [site+1 for site in selected_sites[-1]])  # Convert to 1-indexed sites


class Location:
    def __init__(self, ID: int):
        """
        Function description:
        Initialize a Location object.

        :Input:
        ID: int, ID of the location

        :Output, return or postcondition:
        Make an object of instance location

        :Time complexity:
        O(1)

        :Aux space complexity:
        O(1)
        """
        self.ID = ID
        self.visited = False
        self.discovered = False
        self.time_to_reach = float('inf')
        self.paths = []
        self.previous_location = None

    def __lt__(self, other: 'Location') -> bool:
        """
        Function description:
        Compare two Location objects based on their time_to_reach values. Used in heapq.

        :Input:
        other: Location, the other Location object to compare to

        :Output, return or postcondition:
        bool, True if this Location's time_to_reach is less than the other Location's time_to_reach, else False

        :Time complexity:
        O(1)

        :Aux space complexity:
        O(1)
        """
        return self.time_to_reach < other.time_to_reach

class Path:
    def __init__(self, v: 'Location', x:int):
        """
        Function description:
        Initialize a Path object.

        :Input:
        v: Location, the destination Location
        x: int, the weight of the path

        :Output, return or postcondition:
        Make an object of instance Path

        :Time complexity:
        O(1)

        :Aux space complexity:
        O(1)
        """
        self.v = v
        self.x = x

class Key:
    def __init__(self, k: int, y:int):
        """
        Function description:
        Initialize a Key object.

        :Input:
        k: int, the location ID of key
        y: int, amount of time needed to defeat the monster and retrieve the key

        :Output, return or postcondition:
        Make an object of instance Key

        :Time complexity:
        O(1)

        :Aux space complexity:
        O(1)
        """
        self.k = k
        self.time_to_reach_key = 0
        self.y = y

class FloorGraph:
    def __init__(self, paths: List[List[int]], keys: List[Tuple[int,int]]):
        """
        Function description:
        Initialize a FloorGraph object and construct the graph.

        :Input:
        paths: List[List[int]], list of paths represented as [u, v, x]. u is the source, v is the destination, and
        x is the travel time
        keys: List[List[int]], list of keys represented as [k, y]

        :Output, return or postcondition:
        Initialize the FloorGraph object

        :Time complexity:
        O(|V| + |E|), where |V| is the number of locations and |E| is the total number of paths
        because we are initializing each location and path
        :Aux space complexity:
        O(|V| + |E|) because we are initializing each location and path
        """
        self.locations = []
        self.keys = []
        self.construct_graph(paths, keys)

    def add_location(self, location: 'Location'):
        self.locations.append(location)

    def add_key(self, key: 'Key'):
        self.keys.append(key)

    def add_path(self, u: int, v: int, x: int):
        """
        Function description:
        Add a path from one Location to another in the graph.

        :Input:
        u: int, index of the source Location
        v: int, index of the destination Location
        x: int, travel time of the path

        :Output, return or postcondition:
        add path to locations

        :Time complexity:
        O(1)

        :Aux space complexity:
        O(1)
        """
        path_instance = Path(self.locations[v], x)
        self.locations[u].paths.append(path_instance)

    def construct_graph(self, paths: List[List[int]], keys: List[Tuple[int,int]]):
        """
        Function description:
        Construct the graph with the given paths and keys.

        :Input:
        paths: List[List[int]], list of paths represented as [from_k, v_index, x]
        keys: List[List[int]], list of keys represented as [k, y]

        :Output, return or postcondition:
        construct the graph and initialize Key objects

        :Time complexity:
        O(|V| + |E|), where |V| is the number of locations and |E| is the total number of paths
        because we are initializing each location and path

        :Aux space complexity:
         O(|V| + |E|), because we are initializing each location and path
        """
        for i in range(max(max(paths, key=lambda x: max(x[:2]))[:2]) + 1): #identifies the highest index of a location used in any path.
            self.add_location(Location(i)) # Adding 1 to the maximum index found ensures that there will be enough locations for all locations referenced in the paths.

        for key in keys:
            self.add_key(Key(key[0], key[1]))

        for path in paths:
            self.add_path(*path)

    def dijkstra(self, start_location:'Location'):
        """
        Function description:
        Perform Dijkstra's algorithm using heapq to find the shortest paths in the graph.

        :Input:
        start_location: the starting Location for Dijkstra's algorithm

        :Output, return or postcondition:
        Update the time_to_reach of each location

        :Time complexity:
        The time complexity is O((|E|+|V|) log |V|) because each location is inserted into the priority queue once
        (which costs O(log |V|) time), and for each path, we perform a decrease-key operation on the priority queue
        (which also costs O(log |V|) time). So, the total time complexity is O((|E|+|V|) log |V|).

        :Aux space complexity:
        O(|V|) because we need to store the locations in the priority queue. In the worst case, all locations will be
        in the queue at once,
        """
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

    def get_shortest_path(self, start_index: int, end_index: int) -> Optional[List[int]]:
        """
        Function description:
        Find the shortest path between two keys.

        :Input:
        start_index: int, index of the starting key
        end_index: int, index of the ending key

        :Output, return or postcondition:
        Optional[List[int]], a list of Location indices representing the shortest path, or None if no path exists

        :Time complexity:
        O((|E|+|V|) log |V|), runs Dijkstra’s algorithm, which has a time complexity of O((|E|+|V|) log |V|),
        then traces the shortest path from the end location to the start location, which has a time complexity of O(|V|).

        :Aux space complexity:
        O(|V|), needs to store the locations in the priority queue for Dijkstra’s algorithm (which takes O(|V|) space),
        and it needs to store the shortest path (which also takes O(|V|) space in the worst case).
        """
        start_location = self.locations[start_index]
        end_location = self.locations[end_index]
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
        """
        Function description:
        Reset the visited, discovered, time_to_reach,and previous_location attributes of all locations in the graph.

        :Input:
        None

        :Output, return or postcondition:
        None

        :Time complexity:
        O(|V|), where |V| is the number of locations in the graph. Needs to reset each location in the graph.

        :Aux space complexity:
        O(1), does not use any additional space.
        """
        for location in self.locations:
            location.visited = False
            location.discovered = False
            location.time_to_reach = float('inf')
            location.previous_location = None

    def flip_graph(self):
        """
        Function description:
        Reverse the direction of all paths in the graph.

        :Input:
        None

        :Output, return or postcondition:
        All the paths are now flipped.

        :Time complexity:
        O(|V| + |E|), where |V| is the number of locations and |E| is the number of paths in the graph.
        Needs to create a new location for each location in the original graph (which takes O(|V|) time).
        Then create a new path for each path in the original graph (which takes O(|E|) time).

        :Aux space complexity:
        Auxiliary Space Complexity: O(|V| + |E|), creates a new graph with the same number of locations
        and paths as the original graph.
        """
        flipped_locations = [Location(i) for i in range(len(self.locations))]

        for location in self.locations:
            for path in location.paths:
                flipped_path = Path(flipped_locations[location.ID], path.x)
                flipped_locations[path.v.ID].paths.append(flipped_path)

        self.locations = flipped_locations

    def add_new_location(self, exits: List[int]):
        """
        Function description:
        Adds a new location that is connected to all exits by paths with travel_time 0.

        :Input:
        Exits: List[int], list of exit Locations indexes

        :Output, return or postcondition:
        Adds a new location that is connected to all exits by paths with travel_time 0.

        :Time complexity:
        O(|V|). But originally O(|N|), where |N| is the number of elements in the exits list.
        For each exit, it performs an operation. But there is at most |V| exits.

        :Aux space complexity:
        O(|V|). But originally O(|N|), where |N| is the number of elements in the exits list.
        Creates a new Path instance for each exit_location. But there is at most |V| exits, so the complexity is O(|V|).
        """
        new_location = Location(len(self.locations))
        self.locations.append(new_location)

        for exit_location in exits:
            exit_path = Path(self.locations[exit_location], 0)
            new_location.paths.append(exit_path)

    def get_minimum_distance_to_key(self, start: int):
        """
        Function description:
        Calculate the minimum distance to reach each key from a given start location.

        :Input:
        start: int - index of the starting location

        :Output, return or postcondition:
        Update the time to reach for each key based on the time to reach the location where the key is at.

        :Time complexity:
        O((|E|+|V|) log |V|). But originally O((|E|+|V|) log |V| + |K|), where |E| is the number of edges, |V| is the
        number of vertices, and |K| is the number of keys. This is because it runs Dijkstra’s algorithm, which has a
        time complexity of O((|E|+|V|) log |V|), and then updates the time to reach each key, which takes O(|K|) time.
        But there are at most |V| keys.

        :Aux space complexity:
        O(|V|), as it needs to store the vertices in the priority queue for Dijkstra’s algorithm.
        """
        self.dijkstra(self.locations[start])

        for key in self.keys:
            location = self.locations[key.k]
            key.time_to_reach_key += location.time_to_reach

    def get_minimum_key(self) -> 'Key':
        """
        Function description:
        Find the Key object with the minimum time_to_reach_key + y value.

        :Input:
        None

        :Output, return or postcondition:
        Key: the Key object with the minimum time_to_reach_key + y

        :Time complexity:
        O(|V|). But originally O(|K|), where |K| is the number of keys. Needs to iterate over all keys to find the minimum.
        But there is at most |V| keys so complexity is O(|V|).

        :Aux space complexity:
        O(1), does not use any additional space.
        """
        return min(self.keys, key=lambda key: key.time_to_reach_key + key.y)

    def find_location_to_grab_key(self, start: int, exits: List[int]) -> 'Key':
        """
        Function description:
        Find the Location to grab a key to minimize time. First I'm going to get the minimum distance of each key from a start
        location. Then I would add the time_to_reach of each location to the corresponding key. I then reset the graph because
        the time_to_reach for each location has been changed by the Djikstra's. Then I flip the graph and create a new location
        that is connected to all exits with an edge of weight 0. Now I'm going to get the minimum distance of each key from the
        new location. Then I would add the time_to_reach of each location from the new location to the corresponding key.
        I then find a key that has the minimum combination of time to reach from start, time to reach from the new location,
        and the time to fight monster of that key.

        :Input:
        start: int, index of the starting key
        exits: List[int], list of indices of exit Locations

        :Output, return or postcondition:
        Key: the Key object representing the optimal location to grab a key

        :Time complexity:
        Time Complexity: O((|E|+|V|) log |V|), O((|E|+|V|) log |V| + |K|), where |E| is the number of edges, |V| is the
        number of vertices, and |K| is the number of keys. This is because it runs Dijkstra’s algorithm twice,
        which has a time complexity  of O((|E|+|V|) log |V|) each time, and then finds the minimum key, which takes O(K) time.
        But there are at most |V| keys so the complexity becomes O((|E|+|V|) log |V|)

        :Aux space complexity:
        O(N + E), where E is the number of exits
        """
        self.get_minimum_distance_to_key(start)
        self.reset()
        self.flip_graph()
        self.add_new_location(exits)
        self.get_minimum_distance_to_key(len(self.locations) - 1)
        self.flip_graph()
        self.reset()
        return self.get_minimum_key()

    def climb(self, start: int, exits: List[int]) -> Optional[tuple]:
        """
        Function description:
        Find the location to grab key from. Then get the shortest path from the start to the location to grab key from.
        Then get the shortest path from the location to grab key from to the new location we created in add new location.
        return the total time to get key and the combination of those two paths that we get.
        :Input:
        argv1: int - index of the starting key
        argv2: List[int] - list of indices of exit Locations

        :Output, return or postcondition:
        Tuple or none: a tuple containing the total time and the list of Location indices representing the route,
        or None if no route is found

        :Time complexity:
        Getting the shortest path also uses Dijkstra’s algorithm, so its time complexity is O((V+E)logV). Resetting the keys
        and resetting the graph both have a time complexity of O(V). Therefore, the overall time complexity of climb is
        O((V+E)logV).

        :Aux space complexity:
        O(N + E), where E is the number of exits
        """
        location_to_grab_key = self.find_location_to_grab_key(start, exits)
        route_part1 = self.get_shortest_path(start, location_to_grab_key.k)
        if route_part1 is None:
            return None
        route_part1.pop()  # pop the location where the key is grabbed

        self.reset()
        route_part2 = self.get_shortest_path(location_to_grab_key.k, len(self.locations) - 1)
        if route_part2 is None:
            return None
        route_part2.pop()  # pop the new location from add new location
        total_time = location_to_grab_key.time_to_reach_key + location_to_grab_key.y
        route = route_part1 + route_part2

        self.reset()
        self.delete_new_location()
        self.reset_keys()
        return total_time, route

    def reset_keys(self):
        """
        Function description:
        Reset the time_to_reach attribute of all keys.

        :Input:
        None

        :Output, return or postcondition:
        Resets the time_to_reach for each key

        :Time complexity:
        O(|V|). But originally O(|K|) where |K| is the number of keys.
        This is because it needs to iterate over all keys to reset their time_to_reach attribute.
        But there is at most |V| keys.

        :Aux space complexity:
        O(1), as it does not use any additional space.
        """
        for key in self.keys:
            key.time_to_reach_key = 0

    def delete_new_location(self):
        """
        Function description:
        Delete the new Location from the graph and all the edges connecting to it.

        :Input:
        None

        :Output, return or postcondition:
        Deletes the new Location from the graph and all the edges connecting to it.

        :Time complexity:
        O(|V| + |E|), where |V| is the number of vertices (locations) and |E| is the number of edges (paths).
        This is because it needs to remove the last vertex from the list of vertices (which takes O(1) time),
        and then it needs to iterate over all remaining vertices and their edges to remove any edges that lead to the
        deleted vertex (which takes O(|V| + |E|) time).

        :Aux space complexity:
        O(1), does not use any additonal space.
        """
        new_location = self.locations.pop()

        for location in self.locations:
            location.paths = [path for path in location.paths if path.v != new_location]




