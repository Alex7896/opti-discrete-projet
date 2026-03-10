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


if __name__ == "__main__":
    main()

    # Exemple d'utilisation du 2-opt
    print("\n" + "="*60)
    print("EXEMPLE D'UTILISATION DU 2-OPT")
    print("="*60)

    depot, clients, capacity = read_file("data/data101.vrp")
    solution = random_solution(clients, capacity)

    tester = NeighborhoodTest(solution, depot)

    # Test du 2-opt sur la première route
    print("Test du 2-opt sur la route 0 (positions 1 à 3)")
    tester.test_intra_route_2opt(0, 1, 3, visualize=True)

   