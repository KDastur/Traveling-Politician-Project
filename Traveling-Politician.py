# Made by Kyle Dastur
# 813-557-5053
# Ksdastur1@gmail.com
# https://github.com/KDastur

# This code is made to find a solution to the traveling salesman problem
# This program gives a path for traveling from Iowa to Washington DC, stopping at every US capitol on the way
# This program also outputs the total distance you would have to travel as the crow flies

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

# All 51 capitals are now part of the main calculation (no more outlier removal)
all_states = capitals

# Create a matrix with all capitols, and distances from each other
n = len(all_states)
dist_matrix = [[0.0] * n for _ in range(n)]
for i in range(n):
    for j in range(n):
        if i != j:
            dist_matrix[i][j] = haversine(
                all_states[i]["latitude"], all_states[i]["longitude"],
                all_states[j]["latitude"], all_states[j]["longitude"]
            )

# Index's each state from the original JSON file
def find_index(state_name):
    for i, c in enumerate(all_states):
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

# Calls functions using start and endpoints
start_idx = find_index("Iowa")
end_idx   = find_index("Washington DC")

# Calculates nearest neighbor route, and optimized route
route = nearest_neighbor(dist_matrix, start_idx, end_idx, n)
optimized = two_opt(route, dist_matrix)
final_dist = total_distance(optimized, dist_matrix)

print("\nOptimized Route: \n")
for i, idx in enumerate(optimized):
    c = all_states[idx]
    print(f"  {i+1:>2}. {c['state']} ({c['StateCapitolCity']})")

print(f"\nTotal distance: {final_dist:,.1f} miles")
