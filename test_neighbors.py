from neighbors import intra_route_swap, intra_route_relocate, inter_route_swap, intra_route_2opt
from utils import solution_distance, route_distance
from visualizer import Visualizer


class NeighborhoodTest:
    """Classe pour tester les opérations de voisinage (swap, relocate, etc.)"""

    def __init__(self, solution, depot):
        self.solution = solution
        self.depot = depot
        self.initial_distance = solution_distance(solution, depot)

    def _print_route_clients(self, route):
        """Affiche les IDs des clients dans une route"""
        return [client.id for client in route.clients]

    def _print_route_info(self, route, label=""):
        """Affiche les informations détaillées d'une route"""
        print(f"{label}")
        print(f"  Clients : {self._print_route_clients(route)}")
        print(f"  Charge : {route.load}/{route.capacity}")
        print(f"  Distance : {route_distance(route, self.depot):.2f}")

    def _compare_before_after(self, new_solution, operation_name):
        """Compare la solution avant et après l'opération"""
        new_distance = solution_distance(new_solution, self.depot)
        improvement = self.initial_distance - new_distance

        print(f"\n{'='*60}")
        print(f"COMPARAISON - {operation_name}")
        print(f"{'='*60}")
        print(f"Distance avant : {self.initial_distance:.2f}")
        print(f"Distance après : {new_distance:.2f}")
        print(f"Différence : {improvement:+.2f} ({(improvement/self.initial_distance)*100:+.2f}%)")
        if improvement > 0:
            print("✅ AMÉLIORATION")
        elif improvement < 0:
            print("❌ DÉTÉRIORATION")
        else:
            print("➖ AUCUN CHANGEMENT")
        print(f"{'='*60}\n")

    def test_intra_route_swap(self, route_idx, i, j, visualize=False):
        """
        Test un swap intra-route.
        
        Args:
            route_idx: Index de la route
            i: Position du premier client
            j: Position du second client
            visualize: Si True, affiche la visualisation avant/après
        """
        route = self.solution.routes[route_idx]

        print(f"\n{'='*60}")
        print(f"TEST INTRA-ROUTE SWAP - Route {route_idx}")
        print(f"{'='*60}")

        # Validation
        if i < 0 or j < 0 or i >= len(route.clients) or j >= len(route.clients):
            print("❌ Indices invalides")
            return None

        if i == j:
            print("⚠️ Les deux positions sont identiques")
            return None

        # Avant
        client_i_id = route.clients[i].id
        client_j_id = route.clients[j].id
        print(f"\n📍 AVANT")
        self._print_route_info(route, f"Route {route_idx}")
        print(f"Position {i} : Client {client_i_id}")
        print(f"Position {j} : Client {client_j_id}")

        if visualize:
            Visualizer.plot_single_route(self.solution, self.depot, route_idx)

        # Opération
        print(f"\n🔄 OPÉRATION")
        print(f"Échange Position {i} (Client {client_i_id}) ↔️ Position {j} (Client {client_j_id})")

        new_solution = intra_route_swap(self.solution, route_idx, i, j)

        if new_solution is None:
            print("❌ Swap impossible")
            return None

        # Après
        new_route = new_solution.routes[route_idx]
        print(f"\n📍 APRÈS")
        self._print_route_info(new_route, f"Route {route_idx}")

        if visualize:
            Visualizer.plot_single_route(new_solution, self.depot, route_idx)

        # Comparaison
        self._compare_before_after(new_solution, f"Swap Route {route_idx} Pos {i}↔{j}")

        return new_solution

    def test_intra_route_relocate(self, route_idx, client_pos, new_pos, visualize=False):
        """
        Test un relocate intra-route.
        
        Args:
            route_idx: Index de la route
            client_pos: Position du client à déplacer
            new_pos: Nouvelle position du client
            visualize: Si True, affiche la visualisation avant/après
        """
        route = self.solution.routes[route_idx]

        print(f"\n{'='*60}")
        print(f"TEST INTRA-ROUTE RELOCATE - Route {route_idx}")
        print(f"{'='*60}")

        # Validation
        if client_pos < 0 or new_pos < 0 or client_pos >= len(route.clients) or new_pos > len(route.clients):
            print("❌ Positions invalides")
            return None

        if client_pos == new_pos:
            print("⚠️ La position est identique")
            return None

        # Avant
        client_id = route.clients[client_pos].id
        print(f"\n📍 AVANT")
        self._print_route_info(route, f"Route {route_idx}")
        print(f"Position {client_pos} : Client {client_id} → À déplacer à position {new_pos}")

        if visualize:
            Visualizer.plot_single_route(self.solution, self.depot, route_idx)

        # Opération
        print(f"\n🔄 OPÉRATION")
        print(f"Réassignation Client {client_id} : Position {client_pos} → Position {new_pos}")

        new_solution = intra_route_relocate(self.solution, route_idx, client_pos, new_pos)

        if new_solution is None:
            print("❌ Relocate impossible")
            return None

        # Après
        new_route = new_solution.routes[route_idx]
        print(f"\n📍 APRÈS")
        self._print_route_info(new_route, f"Route {route_idx}")

        if visualize:
            Visualizer.plot_single_route(new_solution, self.depot, route_idx)

        # Comparaison
        self._compare_before_after(new_solution, f"Relocate Route {route_idx} Pos {client_pos}→{new_pos}")

        return new_solution

    def test_intra_route_2opt(self, route_idx, i, j, visualize=False):
        """
        Test un 2-opt intra-route.
        
        Args:
            route_idx: Index de la route
            i: Position de début du segment à inverser
            j: Position de fin du segment à inverser
            visualize: Si True, affiche la visualisation avant/après
        """
        route = self.solution.routes[route_idx]

        print(f"\n{'='*60}")
        print(f"TEST INTRA-ROUTE 2-OPT - Route {route_idx}")
        print(f"{'='*60}")

        # Validation
        if i < 0 or j < 0 or i >= len(route.clients) or j >= len(route.clients):
            print("❌ Indices invalides")
            return None

        if i >= j:
            print("⚠️ Les indices ne forment pas un segment valide")
            return None

        # Avant
        print(f"\n📍 AVANT")
        self._print_route_info(route, f"Route {route_idx}")
        print(f"Segment à inverser : positions {i} à {j}")
        segment_before = [client.id for client in route.clients[i:j+1]]
        print(f"Clients dans le segment : {segment_before}")

        if visualize:
            Visualizer.plot_single_route(self.solution, self.depot, route_idx)

        # Opération
        print(f"\n🔄 OPÉRATION 2-OPT")
        print(f"Inversion du segment [{i}:{j+1}]")

        new_solution = intra_route_2opt(self.solution, route_idx, i, j)

        if new_solution is None:
            print("❌ 2-opt impossible")
            return None

        # Après
        new_route = new_solution.routes[route_idx]
        print(f"\n📍 APRÈS")
        self._print_route_info(new_route, f"Route {route_idx}")
        segment_after = [client.id for client in new_route.clients[i:j+1]]
        print(f"Clients dans le segment : {segment_after}")
        print(f"Inversion : {segment_before} → {segment_after}")

        if visualize:
            Visualizer.plot_single_route(new_solution, self.depot, route_idx)

        # Comparaison
        self._compare_before_after(new_solution, f"2-opt Route {route_idx} [{i}:{j+1}]")

        return new_solution

    def test_inter_route_swap(self, route1_idx, client1_pos, route2_idx, client2_pos, visualize=False):
        """
        Test un swap inter-route.
        
        Args:
            route1_idx: Index de la première route
            client1_pos: Position du client dans la première route
            route2_idx: Index de la deuxième route
            client2_pos: Position du client dans la deuxième route
            visualize: Si True, affiche la visualisation avant/après
        """
        if route1_idx == route2_idx:
            print("⚠️ Routes identiques, utilisation du swap intra-route")
            return self.test_intra_route_swap(route1_idx, client1_pos, client2_pos, visualize)

        route1 = self.solution.routes[route1_idx]
        route2 = self.solution.routes[route2_idx]

        print(f"\n{'='*60}")
        print(f"TEST INTER-ROUTE SWAP - Routes {route1_idx} ↔ {route2_idx}")
        print(f"{'='*60}")

        # Validation
        if (client1_pos < 0 or client1_pos >= len(route1.clients) or
            client2_pos < 0 or client2_pos >= len(route2.clients)):
            print("❌ Positions invalides")
            return None

        # Avant
        client1_id = route1.clients[client1_pos].id
        client2_id = route2.clients[client2_pos].id
        print(f"\n📍 AVANT")
        self._print_route_info(route1, f"Route {route1_idx}")
        self._print_route_info(route2, f"Route {route2_idx}")
        print(f"Client {client1_id} (Route {route1_idx}, pos {client1_pos}) ↔️ Client {client2_id} (Route {route2_idx}, pos {client2_pos})")

        if visualize:
            Visualizer.plot_single_route(self.solution, self.depot, route1_idx)
            Visualizer.plot_single_route(self.solution, self.depot, route2_idx)

        # Opération
        print(f"\n🔄 OPÉRATION INTER-ROUTE SWAP")
        print(f"Échange Client {client1_id} ↔️ Client {client2_id}")

        new_solution = inter_route_swap(self.solution, route1_idx, client1_pos, route2_idx, client2_pos)

        if new_solution is None:
            print("❌ Swap inter-route impossible (contrainte de capacité)")
            return None

        # Après
        new_route1 = new_solution.routes[route1_idx]
        new_route2 = new_solution.routes[route2_idx]
        print(f"\n📍 APRÈS")
        self._print_route_info(new_route1, f"Route {route1_idx}")
        self._print_route_info(new_route2, f"Route {route2_idx}")

        if visualize:
            Visualizer.plot_single_route(new_solution, self.depot, route1_idx)
            Visualizer.plot_single_route(new_solution, self.depot, route2_idx)

        # Comparaison
        self._compare_before_after(new_solution, f"Inter-swap R{route1_idx}↔R{route2_idx}")

        return new_solution

    def test_multiple_operations(self, operations, visualize=False):
        """
        Teste une série d'opérations.
        
        Args:
            operations: Liste de tuples (operation_type, params)
                Ex: [('swap', (0, 0, 1)), ('relocate', (0, 1, 2))]
            visualize: Si True, affiche la visualisation
        """
        current_solution = self.solution
        results = []

        print(f"\n{'*'*60}")
        print(f"TEST MULTIPLE OPÉRATIONS ({len(operations)} opérations)")
        print(f"{'*'*60}")

        for op_type, params in operations:
            if op_type == 'swap':
                current_solution = self.test_intra_route_swap(*params, visualize=visualize)
            elif op_type == 'relocate':
                current_solution = self.test_intra_route_relocate(*params, visualize=visualize)
            elif op_type == '2opt':
                current_solution = self.test_intra_route_2opt(*params, visualize=visualize)
            elif op_type == 'inter_swap':
                current_solution = self.test_inter_route_swap(*params, visualize=visualize)
            else:
                print(f"❌ Opération inconnue : {op_type}")
                continue

            if current_solution is None:
                print(f"⚠️ Arrêt à l'opération {op_type}")
                break

            results.append((op_type, current_solution))

        # Résumé final
        if results:
            final_distance = solution_distance(current_solution, self.depot)
            improvement = self.initial_distance - final_distance
            print(f"\n{'='*60}")
            print(f"RÉSUMÉ FINAL")
            print(f"{'='*60}")
            print(f"Nombre d'opérations réussies : {len(results)}")
            print(f"Distance initiale : {self.initial_distance:.2f}")
            print(f"Distance finale : {final_distance:.2f}")
            print(f"Amélioration totale : {improvement:+.2f} ({(improvement/self.initial_distance)*100:+.2f}%)")
            print(f"{'='*60}\n")

        return current_solution

