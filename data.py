import random
from models import Route, Solution
from models import Client

def read_file(filename):
    clients = []
    depot = None
    capacity = None

    with open(filename, "r") as f:
        lines = f.readlines()

    mode = None

    for line in lines:
        line = line.strip()

        if line.startswith("MAX_QUANTITY"):
            capacity = int(line.split(":")[1])

        elif line.startswith("DATA_DEPOTS"):
            mode = "depot"
            continue

        elif line.startswith("DATA_CLIENTS"):
            mode = "clients"
            continue

        elif mode == "depot" and line.startswith("d"):
            parts = line.split()
            depot = Client(0, parts[1], parts[2], 0)

        elif mode == "clients" and line.startswith("c"):
            parts = line.split()
            client = Client(
                int(parts[0][1:]),
                parts[1],
                parts[2],
                parts[5]  # demande
            )
            clients.append(client)

    return depot, clients, capacity

def random_solution(clients, capacity):
    shuffled = clients[:]
    random.shuffle(shuffled)

    solution = Solution()
    route = Route(capacity)

    for client in shuffled:
        if not route.can_add(client):
            solution.routes.append(route)
            route = Route(capacity)

        route.add_client(client)

    if route.clients:
        solution.routes.append(route)

    return solution