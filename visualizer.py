import matplotlib.pyplot as plt


class Visualizer:

    @staticmethod
    def plot_solution(solution, depot):
        plt.figure()

        # tracer le dépôt
        plt.scatter(depot.x, depot.y, marker='s')
        plt.text(depot.x, depot.y, "Depot")

        for route in solution.routes:
            x_coords = [depot.x]
            y_coords = [depot.y]

            for client in route.clients:
                x_coords.append(client.x)
                y_coords.append(client.y)

            x_coords.append(depot.x)
            y_coords.append(depot.y)

            plt.plot(x_coords, y_coords)
            plt.scatter(x_coords, y_coords)

        plt.title("VRP Solution")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.show()