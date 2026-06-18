def held_karp(graph, hub, destinations):
    nodes = [hub] + destinations
    n = len(nodes)
    node_to_idx = {node: i for i, node in enumerate(nodes)}
    
    memo = {}

    def solve(mask, pos):
        if mask == (1 << n) - 1:
            return graph.distance(nodes[pos], nodes[0]), [nodes[pos], nodes[0]]
        
        state = (mask, pos)
        if state in memo:
            return memo[state]
        
        best_dist = float('inf')
        best_path = []
        
        for next_node in range(n):
            if not (mask & (1 << next_node)):
                d, path = solve(mask | (1 << next_node), next_node)
                dist = graph.distance(nodes[pos], nodes[next_node]) + d
                if dist < best_dist:
                    best_dist = dist
                    best_path = [nodes[pos]] + path
        
        memo[state] = (best_dist, best_path)
        return best_dist, best_path
    
    dist, path = solve(1, 0)
    return path, dist