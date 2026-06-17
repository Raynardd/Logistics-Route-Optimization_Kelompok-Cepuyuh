INF = float("inf")

class WeightedGraph:
    def __init__(self, nodes):
        self.nodes = list(nodes)
        self.index_by_node = {node: index for index, node in enumerate(self.nodes)}
        self.matrix = [
            [ INF for _ in range(len(self.nodes))]
            for _ in range(len(self.nodes))
        ] 

        for index in range(len(self.nodes)):
            self.matrix[index][index]= 0.0

    def add_edge(self, start, end, distance):
        if start not in self.index_by_node:
            raise ValueError(f"Node tidak dikenal: {start}")

        if end not in self.index_by_node:
            raise ValueError(f"Node tidak dikenal: {end}")

        start_index = self.index_by_node[start]
        end_index = self.index_by_node[end]

        self.matrix[start_index][end_index] = distance
        self.matrix[end_index][start_index] = distance

    def distance(self, start, end):
        start_index = self.index_by_node[start]
        end_index = self.index_by_node[end]
        value = self.matrix[start_index][end_index]

        if value == INF:
            raise ValueError(f"Jarak tidak tersedia antara {start} dan {end}")

        return value

    def neighbors(self, node):
        node_index = self.index_by_node[node]
        result = []

        for neighbor_index, distance in enumerate(self.matrix[node_index]):
            if distance != INF and neighbor_index != node_index:
                result.append((self.nodes[neighbor_index], distance))

        return result
    
def build_graph(nodes,edges):
    graph = WeightedGraph(nodes)

    for edge in edges:
        graph.add_edge(edge["start"], edge["end"], edge["distance"])

    return graph

def get_route_distance(graph, route): 
    total = 0.0

    for index in range(len(route)-1):
        total += graph.distance(route[index], route[index+1])
    
    return total

