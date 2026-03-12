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
    # Exemple d'utilisation de l'inter-route swap
    print("\n" + "="*60)
    print("EXEMPLE D'UTILISATION DE L'INTER-ROUTE SWAP")
    print("="*60)

    if len(solution.routes) >= 2:
        # Test inter-route swap entre route 0 et route 1
        if (len(solution.routes[0].clients) > 0 and len(solution.routes[1].clients) > 0):
            print("Test de l'inter-route swap entre route 0 et route 1")
            tester.test_inter_route_swap(0, 0, 1, 0, visualize=True)  # Client 0 de route 0 ↔ Client 0 de route 1
        else:
            print("Pas assez de clients dans les routes pour tester l'inter-route swap")
    else:
        print("Pas assez de routes pour tester l'inter-route swap")

   