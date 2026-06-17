from graph import get_route_distance

def greedy_route(graph, hub,destinations):
    if hub not in graph.index_by_node:
        raise ValueError(f"Hub tidak ditemukan di graf : {hub}")
    
    unvisited = set(destinations)

    if hub in unvisited:
        unvisited.remove(hub)

    route = [hub]
    current = hub

    while unvisited:
        nearest_node = None
        nearest_distance = float("inf")

        for candidate in unvisited:
            distance = graph.distance(current,candidate)

            if distance < nearest_distance:
                nearest_distance = distance
                nearest_node = candidate

        route.append(nearest_node)
        unvisited.remove(nearest_node)
        current = nearest_node

    route.append(hub)

    return route

def run_greedy(graph, hub, packages):
    destinations = sorted({package["destination"] for package in packages})
    route = greedy_route(graph, hub, destinations)
    total_distance = get_route_distance(graph, route)

    return {
        "algorithm": "greedy",
        "route": route,
        "total_distance": total_distance,
    }