from data import read_file, random_solution
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

    # -----------------------------
    # Visualisation de la route 0 avant swap
    # -----------------------------
    route_index = 0

    if len(solution.routes) == 0:
        print("Aucune route dans la solution.")
        return

    if len(solution.routes[route_index].clients) < 2:
        print("La route 0 n'a pas assez de clients pour faire un swap.")
        return

    print(f"\nRoute {route_index} AVANT swap")
    print("Clients :", print_route_clients(solution.routes[route_index]))
    print("Distance route 0 :", route_distance(solution.routes[route_index], depot))

    Visualizer.plot_single_route(solution, depot, route_index)

    # -----------------------------
    # Choix des positions à échanger
    # -----------------------------
    i = 0
    j = 1

    print(f"\nOn échange les positions {i} et {j} dans la route {route_index}")
    print(f"Clients échangés : {solution.routes[route_index].clients[i].id} "
          f"et {solution.routes[route_index].clients[j].id}")

    # -----------------------------
    # Application du swap
    # -----------------------------
    new_solution = intra_route_swap(solution, route_index, i, j)
    print("New clients :", print_route_clients(new_solution.routes[route_index]))
    if new_solution is None:
        print("Swap impossible.")
        return

    # -----------------------------
    # Visualisation de la route 0 après swap
    # -----------------------------
    print(f"\nRoute {route_index} APRÈS swap")
    print("Clients :", print_route_clients(new_solution.routes[route_index]))
    print("Distance route 0 :", route_distance(new_solution.routes[route_index], depot))

    print("\nDistance totale avant :", solution_distance(solution, depot))
    print("Distance totale après :", solution_distance(new_solution, depot))

    Visualizer.plot_single_route(new_solution, depot, route_index)


if __name__ == "__main__":
    main()