from data import read_file, random_solution
from utils import solution_distance, minimum_vehicles
from visualizer import Visualizer

def main():
    depot, clients, capacity = read_file("data/data101.vrp")

    print("Minimum théorique de véhicules :", 
          minimum_vehicles(clients, capacity))

    solution = random_solution(clients, capacity)
    cost = solution_distance(solution, depot)

    print("Nombre de routes :", len(solution.routes))
    print("Distance totale :", cost)

if __name__ == "__main__":
    main()
    Visualizer.plot_solution(random_solution(read_file("data/data101.vrp")[1], read_file("data/data101.vrp")[2]), read_file("data/data101.vrp")[0])