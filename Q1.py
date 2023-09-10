from typing import List, Tuple

def restaurantFinder(min_distance: int, site_revenues: List[int]) -> Tuple[int, List[int]]:
    num_sites = len(site_revenues)
    max_revenue = [0]*num_sites
    chosen_sites = [0]*num_sites

    # Initialize base cases
    max_revenue[0] = site_revenues[0]
    chosen_sites[0] = [0]

    for i in range(1, num_sites):
        # If no restaurant within min_distance km, consider the current site
        if i < min_distance:
            if site_revenues[i] > max_revenue[i-1]:
                max_revenue[i] = site_revenues[i]
                chosen_sites[i] = [i]
            else:
                max_revenue[i] = max_revenue[i-1]
                chosen_sites[i] = chosen_sites[i-1].copy()
        else:
            # Consider the current site and the maximum revenue from sites that are at least min_distance km away
            include_site = site_revenues[i] + (max_revenue[i-min_distance-1] if i-min_distance-1 >= 0 else 0)
            exclude_site = max_revenue[i-1]

            if include_site > exclude_site:
                max_revenue[i] = include_site
                if i-min_distance-1 >= 0:
                    chosen_sites[i] = chosen_sites[i-min_distance-1].copy()
                else:
                    chosen_sites[i] = []
                chosen_sites[i].append(i)
            else:
                max_revenue[i] = exclude_site
                chosen_sites[i] = chosen_sites[i-1].copy()

    return (max_revenue[-1], [site+1 for site in chosen_sites[-1]])  # Convert to 1-indexed sites

if __name__ == "__main__":
    print(restaurantFinder(1,[50, 10, 12, 65, 40, 95, 100, 12, 20, 30]))
    print(restaurantFinder(2,[50, 10, 12, 65, 40, 95, 100, 12, 20, 30]))
    print( restaurantFinder(3,[50, 10, 12, 65, 40, 95, 100, 12, 20, 30]))
    print(restaurantFinder(7,[50, 10, 12, 65, 40, 95, 100, 12, 20, 30]))
    print(restaurantFinder(0,[50, 10, 12, 65, 40, 95, 100, 12, 20, 30]))
