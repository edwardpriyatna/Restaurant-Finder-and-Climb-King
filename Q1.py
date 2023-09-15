from typing import List, Tuple

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

