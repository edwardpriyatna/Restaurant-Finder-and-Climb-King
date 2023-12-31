from typing import List, Tuple, Optional
import heapq
def restaurantFinder(d: int, site_list: List[int]) -> Tuple[int, List[int]]:
    """
    Function description:
    This function assists a fast food chain in selecting optimal sites for opening restaurants. The selection is done
    such that no two restaurants are within 'd' km of each other and the total revenue is maximized.

    Approach description:
    The function uses a dynamic programming approach. It maintains two lists: 'total_revenue' and 'selected_sites'. The
    'total_revenue' list stores the maximum revenue that can be obtained for each site. The 'selected_sites' list stores
    the sites that are selected to achieve this maximum revenue. For each site, the function considers two options:
    including the current site or excluding it. It compares the total revenue obtained from these two options and chooses
    the one with maximum revenue. After finding the maximum total revenue for all sites, the function reconstructs the
    list of selected sites by iterating over the 'selected_sites' list in reverse order.

    :Input:
    d: The minimum distance between any two chosen sites.
    site_list: A list of revenues for each site.

    :Output, return or postcondition:
    The function returns a tuple with two elements: The maximum total revenue that can be obtained and a list of the
    chosen sites that are 1-indexed.

    :Time complexity:
    O(N), where N is the number of potential sites. This is because the function makes a single pass over the list of
    potential sites. For each site, it performs a constant amount of work.

    :Aux space complexity:
    O(N). The function maintains two lists 'total_revenue' and 'selected_sites', each of which has a length of N. These
    lists are used to store intermediate results during computation. Since these lists have a size proportional to the
    number of sites, the complexity is O(N).
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

    return (total_revenue.pop(), [site+1 for site in selected_sites[-1]])  # Convert to 1-indexed sites

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
    def __init__(self, paths: List[Tuple[int,int,int]], keys: List[Tuple[int,int]]):
        """
        Function description:
        Initialize a FloorGraph object and construct the graph.

        Approach description:
        I initialize the attributes then call construct_graph.

        :Input:
        paths: List[Tuple[int,int,int]], list of paths represented as [u, v, x]. u is the source, v is the destination,
        and x is the travel time
        keys: List[List[int,int]], list of keys represented as [k, y]

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

    def construct_graph(self, paths: List[Tuple[int,int,int]], keys: List[Tuple[int,int]]):
        """
        Function description:
        Construct the graph with the given paths and keys.

        Approach description:
        I identify the highest index of a location entered. Add 1 to the highest index to ensure that it loops
        through all of them. Then I added the locations to self.locations, added keys to self.keys, and added the path
        to each location.

        :Input:
        paths: List[Tuple[int,int,int]], list of paths represented as [u, v, x]
        keys: List[Tuple[int,int]], list of keys represented as [k, y]

        :Output, return or postcondition:
        construct the graph and initialize Key objects

        :Time complexity:
        O(|V| + |E|), where |V| is the number of locations and |E| is the total number of paths
        because we are initializing each location and path

        :Aux space complexity:
        O(|V| + |E|), because we are initializing each location and path
        """
        for i in range(max(max(paths, key=lambda x: max(x[:2]))[:2]) + 1):
            self.locations.append(Location(i))

        for key in keys:
            self.keys.append(Key(key[0], key[1]))

        for path in paths:
            u, v, x = path
            self.locations[u].paths.append(Path(self.locations[v], x))

    def dijkstra(self, start_index:int):
        """
        Function description:
        Perform Dijkstra's algorithm using heapq to update the time_to_reach for each location.

        :Input:
        start_index: int, the starting location index for Dijkstra's algorithm

        :Output, return or postcondition:
        Update the time_to_reach of each location

        :Time complexity:
        O(|E| log(|V|)). |V| is the number of locations and |E| is the total number of paths. Because each location is
        inserted into the priority queue once which costs O(log |V|) time. For each path, we perform a decrease-key
        operation on the heap which also costs O(log |V|) time. So, the total time complexity is O(|E| log(|V|)).

        :Aux space complexity:
        O(|V|+|E|) because we need to store the locations in the priority queue. In the worst case, all locations will
        be in the queue at once.
        """
        start_location=self.locations[start_index]
        queue = []
        start_location.time_to_reach = 0
        heapq.heappush(queue, start_location)

        while queue:
            current_location = heapq.heappop(queue)
            if current_location.visited:
                continue
            current_location.visited = True

            for path in current_location.paths:
                tentative_time = current_location.time_to_reach + path.x
                if tentative_time < path.v.time_to_reach:
                    path.v.time_to_reach = tentative_time
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
        O(|E| log(|V|)), runs Dijkstra’s algorithm, which has a time complexity of O(|E| log(|V|)).

        :Aux space complexity:
        O(|V|+|E|), needs to run Dijkstra's.
        """
        end_location = self.locations[end_index]
        self.dijkstra(start_index)
        if end_location.time_to_reach == float('inf'):
            return None
        path = []
        current_location = end_location
        while current_location is not None:
            path.append(current_location.ID)
            current_location = current_location.previous_location

        return list(reversed(path)) #reverse the path because this function actually returns the reversed sequences

    def reset(self):
        """
        Function description:
        Reset the visited, discovered, time_to_reach,and previous_location attributes of all locations in the graph.

        :Input:
        None

        :Output, return or postcondition:
        Reset the visited, discovered, time_to_reach,and previous_location attributes of all locations in the graph.

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
        O(|V|+|E|), where |V| is the number of locations and |E| is the number of paths in the graph.
        Needs to create a new location for each location in the original graph (which takes O(|V|) time).
        Then create a new path for each path in the original graph (which takes O(|E|) time).

        :Aux space complexity:
        O(|V| + |E|), creates a new graph with the same number of locations and paths as the original graph.
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
        Adds a new location that is connected to all exits by paths with travel_time 0. But doesn't connect the other
        way around.

        :Input:
        Exits: List[int], list of exit Locations indexes

        :Output, return or postcondition:
        Adds a new location that is connected to all exits by paths with travel_time 0.

        :Time complexity:
        O(|V|). |V| is the number of locations. For each exit, connect the new location to that exit.
        But there is at most |V| exits.

        :Aux space complexity:
        O(|V|). Creates a new Path instance for each exit_location. But there is at most |V| exits, so the
        complexity is O(|V|).
        """
        new_location = Location(len(self.locations))
        self.locations.append(new_location)

        for exit_location in exits: #adding connections to the exit locations
            new_location.paths.append(Path(self.locations[exit_location], 0))

    def get_minimum_time_to_key(self, start_index: int):
        """
        Function description:
        Calculate the minimum time to reach each key from a given start location.

        :Input:
        start_index: int - index of the starting location

        :Output, return or postcondition:
        Update the time to reach for each key based on the time to reach the location where the key is at.

        :Time complexity:
        O(|E|log(|V|)). Where |E| is the number of edges and |V| is the number of vertices. Runs Dijkstra’s, which has
        time complexity of O(|E| log(|V|)), and then updates the time to reach each key, which takes O(|V|) time.

        :Aux space complexity:
        O(|V|+|E|), as it runs Dijkstra’s algorithm.
        """
        self.dijkstra(start_index)

        for key in self.keys:
            location = self.locations[key.k]
            key.time_to_reach_key += location.time_to_reach

    def find_location_to_grab_key(self, start: int, exits: List[int]) -> 'Key':
        """
        Function description:
        Find the Location to grab a key to minimize time.

        Approach description:
        First I'm going to get the minimum time of each key from a start location. Then I would add the time_to_reach of
        each location to the corresponding key. I then reset the graph because the time_to_reach for each location has
        been changed by the Dijkstra's. Then I flip the graph and create a new location that is connected to all exits
        with an edge of weight 0. Now I'm going to get the minimum time of each key from the new location. Then I would
        add the time_to_reach of each location from the new location to the corresponding key. I then find a key that
        has the minimum combination of time to reach from start, time to reach from the new location, and the time to
        fight monster of that key.

        :Input:
        start: int, index of the starting key
        exits: List[int], list of indices of exit Locations

        :Output, return or postcondition:
        Key: the Key object representing the optimal location to grab a key

        :Time complexity:
        Time Complexity: O(|E|log(|V|)), where |E| is the number of edges, |V| is the number of vertices. Runs Dijkstra’s
        twice, with time complexity of O(|E| log(|V|)). Then finds the minimum key, which takes O(|V|) time.

        :Aux space complexity:
        O(|V| + |E|), because it runs Djikstra's
        """
        self.get_minimum_time_to_key(start)
        self.reset()
        self.flip_graph()
        self.add_new_location(exits)
        self.get_minimum_time_to_key(len(self.locations) - 1)
        self.flip_graph() # also flips the connections to the new location which would be beneficial in climb
        self.reset()
        return min(self.keys, key=lambda key: key.time_to_reach_key + key.y)

    def climb(self, start: int, exits: List[int]) -> Optional[tuple]:
        """
        Function description:
        The main climb function.

        Approach description:
        Find the location to grab key from (see find_location_to_grab_key). Then get the shortest path from the start to
        the location to grab key from. Then get the shortest path from the location to grab key from to the new location
        we created in add new location. return the total time to get key and the combination of those two paths that we got.
        :Input:
        argv1: int - index of the starting key
        argv2: List[int] - list of indices of exit Locations

        :Output, return or postcondition:
        Tuple or none: a tuple containing the total time and the list of Location indices representing the route,
        or None if no route is found

        :Time complexity:
        O(|E|log(|V|)). Finding the location to grab the key and getting the shortest path both uses Dijkstra’s, the time
        complexity are both O(|E|log(|V|)). Combined, the time complexity is O(|E|log(|V|)). Resetting the graph, delete new
        location, and resetting weight all have time complexity of O(|V|). So, the time complexity is O(|E|log(|V|)).

        :Aux space complexity:
        O(|V|+|E|), from running Djikstra's and deleting new location.
        """
        location_to_grab_key = self.find_location_to_grab_key(start, exits)
        route_part1 = self.get_shortest_path(start, location_to_grab_key.k)
        if route_part1 is None:
            return None
        route_part1.pop()  # pop the location where the key is grabbed

        self.reset()
        route_part2 = self.get_shortest_path(location_to_grab_key.k, len(self.locations) - 1) #getting shortest path to new location
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
        Reset the time_to_reach_key attribute of all keys.

        :Input:
        None

        :Output, return or postcondition:
        Resets the time_to_reach for each key

        :Time complexity:
        O(|V|). But originally O(|K|) where |K| is the number of keys. Needs to iterate over all keys to reset their
        time_to_reach_key attribute. But there is at most |V| keys.

        :Aux space complexity:
        O(1), as it does not use any additional space.
        """
        for key in self.keys:
            key.time_to_reach_key = 0

    def delete_new_location(self):
        """
        Function description:
        Delete the new Location that generated from add new location from the graph and all the edges connecting to it.

        :Input:
        None

        :Output, return or postcondition:
        Deletes the new Location from the graph and all the edges connecting to it.

        :Time complexity:
        O(|V| + |E|), where |V| is the number of vertices (locations) and |E| is the number of edges (paths).
        This is because it needs to remove the last vertex from the list of vertices (which takes O(1) time),
        and then it needs to iterate over all remaining vertices and their edges to remove any edges that leads to the
        deleted vertex (which takes O(|V| + |E|) time).

        :Aux space complexity:
        O(1), does not use any additional space.
        """
        new_location = self.locations.pop()

        for location in self.locations: # deleting all connections to the new location
            location.paths = [path for path in location.paths if path.v != new_location]






