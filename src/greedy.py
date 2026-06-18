from graph import get_route_distance

def greedy_route(graph, hub, destinations):
    if hub not in graph.index_by_node:
        raise ValueError(f"Hub tidak ditemukan di graf : {hub}")
    
    unvisited = set(destinations)

    if hub in unvisited:
        unvisited.remove(hub)

    def backtrack_search(current_node, unvisited_left, current_path):
        if not unvisited_left:
            try:
                graph.distance(current_node, hub)
                return current_path + [hub]
            except ValueError:
                return None 
        
        valid_neighbors = []
        for candidate in unvisited_left:
            try:
                dist = graph.distance(current_node, candidate)
                valid_neighbors.append((dist, candidate))
            except ValueError:
                pass 
                
        valid_neighbors.sort(key=lambda x: x[0])
        
        for dist, next_node in valid_neighbors:
            unvisited_left.remove(next_node)
            
            result_route = backtrack_search(next_node, unvisited_left, current_path + [next_node])
            
            if result_route is not None:
                return result_route

            unvisited_left.add(next_node)
            
        return None

    final_route = backtrack_search(hub, unvisited, [hub])
    
    if final_route is None:
        raise ValueError("Graf terputus")
        
    return final_route

def run_greedy(graph, hub, packages):
    destinations = sorted({package["destination"] for package in packages})
    route = greedy_route(graph, hub, destinations)
    total_distance = get_route_distance(graph, route)

    return {
        "algorithm": "greedy",
        "route": route,
        "total_distance": total_distance,
    }