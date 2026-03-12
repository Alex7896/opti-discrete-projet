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

def inter_route_swap(solution, route1_idx, client1_pos, route2_idx, client2_pos):
    """Swap clients between two different routes, respecting capacity constraints."""
    if route1_idx == route2_idx:
        return intra_route_swap(solution, route1_idx, client1_pos, client2_pos)

    new_solution = solution.copy()
    route1 = new_solution.routes[route1_idx]
    route2 = new_solution.routes[route2_idx]

    # Validation
    if (client1_pos < 0 or client1_pos >= len(route1.clients) or
        client2_pos < 0 or client2_pos >= len(route2.clients)):
        return None

    client1 = route1.clients[client1_pos]
    client2 = route2.clients[client2_pos]

    # Check capacity constraints
    new_load1 = route1.load - client1.demand + client2.demand
    new_load2 = route2.load - client2.demand + client1.demand

    if new_load1 > route1.capacity or new_load2 > route2.capacity:
        return None

    # Perform swap
    route1.clients[client1_pos] = client2
    route2.clients[client2_pos] = client1

    # Update loads
    route1.load = new_load1
    route2.load = new_load2

    return new_solution

def random_inter_route_swap(solution):
    """Randomly swap clients between two different routes."""
    if len(solution.routes) < 2:
        return None

    # Select two different routes
    route_indices = list(range(len(solution.routes)))
    route1_idx, route2_idx = random.sample(route_indices, 2)

    route1 = solution.routes[route1_idx]
    route2 = solution.routes[route2_idx]

    if not route1.clients or not route2.clients:
        return None

    client1_pos = random.randint(0, len(route1.clients) - 1)
    client2_pos = random.randint(0, len(route2.clients) - 1)

    return inter_route_swap(solution, route1_idx, client1_pos, route2_idx, client2_pos)

def intra_route_2opt(solution, route_idx, i, j):
    """
    Apply 2-opt operation within a route.
    Reverses the segment between positions i and j (inclusive).
    """
    new_solution = solution.copy()
    route = new_solution.routes[route_idx]

    # Validation
    if i < 0 or j < 0 or i >= len(route.clients) or j >= len(route.clients):
        return None

    if i >= j:
        return new_solution  # No change needed

    # Reverse the segment from i to j (inclusive)
    route.clients[i:j+1] = route.clients[i:j+1][::-1]

    return new_solution

def random_intra_route_2opt(solution):
    """
    Randomly apply 2-opt within a route.
    Selects two random positions and reverses the segment between them.
    """
    valid_routes = [idx for idx, route in enumerate(solution.routes) if len(route.clients) >= 4]

    if not valid_routes:
        return None

    route_idx = random.choice(valid_routes)
    route = solution.routes[route_idx]

    # Select two different positions with enough space for meaningful reversal
    i, j = sorted(random.sample(range(len(route.clients)), 2))

    # Ensure minimum segment length of 2
    if j - i < 1:
        j = min(j + 1, len(route.clients) - 1)

    return intra_route_2opt(solution, route_idx, i, j)