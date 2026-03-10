from data import read_file, random_solution
from test_neighbors import NeighborhoodTest
from utils import solution_distance, minimum_vehicles, route_distance
from visualizer import Visualizer
from neighbors import intra_route_swap


def print_route_clients(route):
    return [client.id for client in route.clients]


def main():
    depot, clients, capacity = read_file("data/data101.vrp")

    print("Minimum théorique de véhicules :", minimum_vehicles(clients, capacity))

    solution = random_solution(clients, capacity)
    cost = solution_distance(solution, depot)

    print("Nombre de routes :", len(solution.routes))
    print("Distance totale :", cost)

    tester = NeighborhoodTest(solution, depot)
    tester.test_intra_route_relocate(0, 1, 5, visualize=True)

if __name__ == "__main__":
    main()