import matplotlib.pyplot as plt


class Visualizer:
    @staticmethod
    def _draw_route(route, depot, color='blue', route_id=None, annotate_order=False):
        """Helper to draw a single route on the current figure."""
        # depot first
        x_coords = [depot.x]
        y_coords = [depot.y]

        for client in route.clients:
            x_coords.append(client.x)
            y_coords.append(client.y)

        x_coords.append(depot.x)
        y_coords.append(depot.y)

        label = f"Route {route_id}" if route_id is not None else None
        plt.plot(x_coords, y_coords, color=color, linewidth=2, marker='o',
                 markersize=8, markerfacecolor=color, markeredgecolor='black',
                 label=label)

        # annotate clients with improved visibility
        for idx, client in enumerate(route.clients):
            # draw id above the point with a slight vertical offset and white bbox
            plt.text(client.x, client.y + 0.5, str(client.id), fontsize=9,
                     ha='center', va='bottom',
                     bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))
            if annotate_order:
                # sequence number below the point with offset and background
                plt.text(client.x, client.y - 0.5, f"({idx+1})", fontsize=8,
                         ha='center', va='top',
                         bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))

        # arrows to indicate direction
        for k in range(len(x_coords) - 1):
            plt.arrow(x_coords[k], y_coords[k],
                      x_coords[k+1] - x_coords[k], y_coords[k+1] - y_coords[k],
                      head_width=1.5, head_length=1.5, fc=color, ec=color, alpha=0.6)

    @staticmethod
    def plot_solution(solution, depot):
        plt.figure(figsize=(10, 8))

        # plot depot
        plt.scatter(depot.x, depot.y, marker='s', s=200, color='red', zorder=5)
        plt.text(depot.x, depot.y, "Depot", fontsize=12, fontweight='bold',
                 ha='center', va='bottom')

        colors = ['blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive']
        for i, route in enumerate(solution.routes):
            Visualizer._draw_route(route, depot, color=colors[i % len(colors)],
                                   route_id=i+1)

        plt.title("VRP Solution - All Routes")
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_routes_separately(solution, depot):
        """Display each route in its own figure"""
        colors = ['blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive']
        for i, route in enumerate(solution.routes):
            plt.figure(figsize=(8, 6))
            # depot
            plt.scatter(depot.x, depot.y, marker='s', s=200, color='red', zorder=5)
            plt.text(depot.x, depot.y, "Depot", fontsize=12, fontweight='bold',
                     ha='center', va='bottom')

            Visualizer._draw_route(route, depot, color=colors[i % len(colors)],
                                   annotate_order=True)
            plt.title(f"Route {i+1} - {len(route.clients)} clients - Load: {route.load}/{route.capacity}")
            plt.xlabel("X Coordinate")
            plt.ylabel("Y Coordinate")
            plt.grid(True, alpha=0.3)
            plt.axis('equal')
            plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_single_route(solution, depot, index):
        """Plot only the route at the given index (0-based)."""
        if index < 0 or index >= len(solution.routes):
            raise IndexError(f"Route index {index} out of range (0..{len(solution.routes)-1})")
        route = solution.routes[index]
        plt.figure(figsize=(8, 6))
        plt.scatter(depot.x, depot.y, marker='s', s=200, color='red', zorder=5)
        plt.text(depot.x, depot.y, "Depot", fontsize=12, fontweight='bold',
                 ha='center', va='bottom')
        Visualizer._draw_route(route, depot, color='blue', annotate_order=True)
        plt.title(f"Single Route {index+1} - {len(route.clients)} clients - Load: {route.load}/{route.capacity}")
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.grid(True, alpha=0.3)
        plt.axis('equal')
        plt.tight_layout()
        plt.show()