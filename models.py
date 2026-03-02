class Client:
    def __init__(self, id, x, y, demand):
        self.id = id
        self.x = float(x)
        self.y = float(y)
        self.demand = int(demand)


class Route:
    def __init__(self, capacity):
        self.capacity = capacity
        self.clients = []
        self.load = 0

    def can_add(self, client):
        return self.load + client.demand <= self.capacity

    def add_client(self, client):
        self.clients.append(client)
        self.load += client.demand


class Solution:
    def __init__(self):
        self.routes = []
        self.total_distance = 0