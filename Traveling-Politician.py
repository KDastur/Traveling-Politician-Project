import json
from math import radians, sin, cos, sqrt, atan2

with open("state_capitals_with_coords-Copy.json") as f:
    capitals = json.load(f)

# Equation for determining distance on a spherical plane using coordinates
def haversine(lat1, lon1, lat2, lon2):
    R = 3956
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1-a))

# Removing Hawaii and Alaska from main calculation (Outliers)
contiguous = [c for c in capitals if c["state"] not in ("Hawaii", "Alaska")]
hawaii = next(c for c in capitals if c["state"] == "Hawaii")
alaska = next(c for c in capitals if c["state"] == "Alaska")

# Create a matrix with all capitols, and distances from each other
n = len(contiguous)
dist_matrix = [[0.0] * n for _ in range(n)]
for i in range(n):
    for j in range(n):
        if i != j:
            dist_matrix[i][j] = haversine(
                contiguous[i]["latitude"], contiguous[i]["longitude"],
                contiguous[j]["latitude"], contiguous[j]["longitude"]
            )

# Index's each state from the original JSON file
def find_index(state_name):        
    for i, c in enumerate(contiguous):
        if c["state"] == state_name:
            return i
    raise ValueError(f"'{state_name}' not found")

# Finds closest unvisited neighboring capitol to the current one
# Keeps track of the route
def nearest_neighbor(dist_matrix, start, end, n):   
    unvisited = set(range(n)) - {start, end}
    route = [start]
    current = start
    while unvisited:
        nearest = min(unvisited, key=lambda x: dist_matrix[current][x])
        route.append(nearest)
        unvisited.remove(nearest)
        current = nearest
    route.append(end)
    return route

# Measures total distance using original route and distance matrix
def total_distance(route, dist_matrix):              
    return sum(dist_matrix[route[i]][route[i+1]] for i in range(len(route)-1))

# Modifies route to reduce total distance
# Removes any crossing paths and improves it
def two_opt(route, dist_matrix):                     
    best = route[:]
    improved = True
    while improved:
        improved = False
        for i in range(1, len(best) - 2):
            for j in range(i + 1, len(best) - 1):
                new_route = best[:i] + best[i:j+1][::-1] + best[j+1:]
                if total_distance(new_route, dist_matrix) < total_distance(best, dist_matrix):
                    best = new_route
                    improved = True
    return best

# Finds nearest stop for Alaska and Hawaii, returns the nearest state and best distance 
def find_nearest_stop(outlier, route_list, capitals_list):
    best_dist = float('inf')
    best_stop = None
    for idx in route_list:
        d = haversine(
            outlier["latitude"], outlier["longitude"],
            capitals_list[idx]["latitude"], capitals_list[idx]["longitude"]
        )
        if d < best_dist:
            best_dist = d
            best_stop = capitals_list[idx]["state"]
    return best_stop, best_dist

# Calls functions using start and endpoints
start_idx = find_index("Iowa")
end_idx   = find_index("Washington DC")

# Caluclates nearest neighbor route, and optimized route
route = nearest_neighbor(dist_matrix, start_idx, end_idx, n)
optimized = two_opt(route, dist_matrix)
final_dist = total_distance(optimized, dist_matrix)


print("\nOptimized Route (Not including Alaska and Hawaii)\n")
for i, idx in enumerate(optimized):
    c = contiguous[idx]
    print(f"  {i+1:>2}. {c['state']} ({c['StateCapitolCity']})")

hawaii_nearest, hawaii_dist = find_nearest_stop(hawaii, optimized, contiguous)
alaska_nearest, alaska_dist = find_nearest_stop(alaska, optimized, contiguous)

hawaii_roundtrip = hawaii_dist * 2
alaska_roundtrip = alaska_dist * 2
total_with_outliers = final_dist + hawaii_roundtrip + alaska_roundtrip

# Final output, includes distance with and without including hawaii and alaska
print(f"\nOutlier States Detours (round trip from nearest stop)")
print(f"Hawaii:  nearest stop is {hawaii_nearest}, "
      f"round trip = {hawaii_roundtrip:,.1f} miles")
print(f"Alaska:  nearest stop is {alaska_nearest}, "
      f"round trip = {alaska_roundtrip:,.1f} miles")
print(f"\nDistance without Alaska & Hawaii:   {final_dist:,.1f} miles")
print(f"Total with all 51:    = {total_with_outliers:,.1f} miles")
