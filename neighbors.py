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

def intra_route_relocate(solution, route_idx, client_pos, new_pos):
    """Relocate a client within the same route.
    Removes client at client_pos and inserts it at new_pos."""
    new_solution = solution.copy()
    route = new_solution.routes[route_idx]

    if client_pos == new_pos:
        return new_solution

    if client_pos < 0 or new_pos < 0 or client_pos >= len(route.clients) or new_pos > len(route.clients):
        return None

    client = route.clients.pop(client_pos)
    route.clients.insert(new_pos, client)
    return new_solution

def random_intra_route_relocate(solution):
    """Randomly select a route and relocate a client within it."""
    valid_routes = [idx for idx, route in enumerate(solution.routes) if len(route.clients) >= 2]

    if not valid_routes:
        return None

    route_idx = random.choice(valid_routes)
    route = solution.routes[route_idx]

    client_pos = random.randint(0, len(route.clients) - 1)
    new_pos = random.randint(0, len(route.clients) - 1)

    return intra_route_relocate(solution, route_idx, client_pos, new_pos)