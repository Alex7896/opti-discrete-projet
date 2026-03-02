import math

def distance(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)


def route_distance(route, depot):
    total = 0
    prev = depot

    for client in route.clients:
        total += distance(prev, client)
        prev = client

    total += distance(prev, depot)
    return total


def solution_distance(solution, depot):
    total = 0
    for route in solution.routes:
        total += route_distance(route, depot)

    solution.total_distance = total
    return total

def minimum_vehicles(clients, capacity):
    total_demand = sum(c.demand for c in clients)
    return math.ceil(total_demand / capacity)