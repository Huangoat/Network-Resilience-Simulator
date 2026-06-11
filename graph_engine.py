import random

class GraphEngine:
    def __init__(self, num_nodes=10, connection_prob=0.4):
        self.num_nodes = num_nodes
        self.prob = connection_prob
        self.disabled_nodes = set()
        self.positions = {}
        self.edges = []
        self.generate_graph()

    def generate_graph(self):
        self.disabled_nodes.clear()
        self.positions = {i: (random.uniform(0.1, 0.9), random.uniform(0.1, 0.9)) for i in range(self.num_nodes)}
        
        connected = False
        attempt_counter = 0
        while not connected:
            attempt_counter += 1
            self.edges = []
            for i in range(self.num_nodes):
                for j in range(i + 1, self.num_nodes):
                    if random.random() < self.prob:
                        weight = random.randint(1, 10)
                        self.edges.append((i, j, weight))
            
            connected = len(self.get_connected_components(set(range(self.num_nodes)), self.edges)) == 1
            if attempt_counter > 50:
                self.prob += 0.1 

    def get_adjacency_list(self, active_nodes, active_edges):
        adj = {n: [] for n in active_nodes}
        for u, v, w in active_edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
        return adj

    # BFS to generate connected components efficiently
    def get_connected_components(self, active_nodes, active_edges):
        if not active_nodes: return []
        adj_list = self.get_adjacency_list(active_nodes, active_edges)
        visited = set()
        components = []
        for node in active_nodes:
            if node not in visited:
                component = []
                queue = [node]
                visited.add(node)
                while queue:
                    current = queue.pop(0)
                    component.append(current)
                    for neighbor, _ in adj_list[current]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
                components.append(component)
        return components

    def reconnect_graph(self, active_nodes, active_edges):
        components = self.get_connected_components(active_nodes, active_edges)
        if len(components) > 1:
            for i in range(len(components) - 1):
                node1 = components[i][0]
                node2 = components[i+1][0]
                weight = random.randint(1, 10)
                self.edges.append((node1, node2, weight))
                active_edges.append((node1, node2, weight))

    # Kruskal's algorithm to generate MST
    def get_minimum_spanning_tree(self, active_nodes, active_edges):
        mst_edges = []
        sorted_edges = sorted(active_edges, key=lambda e: e[2])
        parent = {n: n for n in active_nodes}
        
        def find(i):
            if parent[i] == i: return i
            parent[i] = find(parent[i])
            return parent[i]
            
        def union(i, j):
            root_i = find(i)
            root_j = find(j)
            if root_i != root_j:
                parent[root_i] = root_j
                return True
            return False

        for u, v, w in sorted_edges:
            if union(u, v):
                mst_edges.append((u, v, w))
        return mst_edges

    # Djikstra's algorithm for shortest path
    def get_average_shortest_path(self, active_nodes, active_edges):
        if len(active_nodes) <= 1: return 0
        adj_list = self.get_adjacency_list(active_nodes, active_edges)
        total_distance = 0
        paths_counted = 0
        
        for start_node in active_nodes:
            distances = {n: float('inf') for n in active_nodes}
            distances[start_node] = 0
            unvisited = set(active_nodes)
            
            while unvisited:
                current = min(unvisited, key=lambda node: distances[node])
                if distances[current] == float('inf'): break
                unvisited.remove(current)
                
                for neighbor, weight in adj_list[current]:
                    if neighbor in unvisited:
                        new_dist = distances[current] + weight
                        if new_dist < distances[neighbor]:
                            distances[neighbor] = new_dist
                            
            for end_node in active_nodes:
                if start_node != end_node and distances[end_node] != float('inf'):
                    total_distance += distances[end_node]
                    paths_counted += 1
                    
        return total_distance / paths_counted if paths_counted > 0 else 0