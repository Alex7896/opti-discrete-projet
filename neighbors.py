def intra_route_swap(solution, route_idx, i, j):
    new_solution = solution.copy()
    route = new_solution.routes[route_idx]

    if i == j:
        return new_solution

    if i < 0 or j < 0 or i >= len(route.clients) or j >= len(route.clients):
        return None

    route.clients[i], route.clients[j] = route.clients[j], route.clients[i]
    return new_solution

def random_intra_route_swap(solution):
    valid_routes = [idx for idx, route in enumerate(solution.routes) if len(route.clients) >= 2]

    if not valid_routes:
        return None

    route_idx = random.choice(valid_routes)
    route = solution.routes[route_idx]

    i, j = random.sample(range(len(route.clients)), 2)

    return intra_route_swap(solution, route_idx, i, j)