from utils import group_package_weight_by_destination

SERVER_COST_PER_MS = 50.0
LOAD_PENALTY_FACTOR = 0.5

def calculate_liter_per_km(vehicle, current_weight):
    capacity = vehicle["capacity_kg"]

    if capacity <=0:
        raise ValueError("Kapasitas kendaraan harus lebih dari 0.")
    
    base_liter_per_km = 1 / vehicle["km_per_liter"]
    load_ratio = max(0.0, min(current_weight / capacity, 1.0))

    return base_liter_per_km * (1 + LOAD_PENALTY_FACTOR * load_ratio)

def calculate_route_fuel_cost(graph, route, packages, vehicle, fuel_price):
    remaining_weight_by_destination = group_package_weight_by_destination(packages)
    current_weight = sum(remaining_weight_by_destination.values())

    if current_weight > vehicle["capacity_kg"]:
        raise ValueError(
            f"Total berat paket {current_weight:.2f} kg melebihi kapasitas "
            f"{vehicle['name']} ({vehicle['capacity_kg']:.2f} kg)."
        )

    total_fuel_liter = 0.0
    total_fuel_cost = 0.0
    details = []

    for index in range(len(route) - 1):
        start = route[index]
        end = route[index + 1]
        distance = graph.distance(start, end)

        liter_per_km = calculate_liter_per_km(vehicle, current_weight)
        fuel_liter = distance * liter_per_km
        fuel_cost = fuel_liter * fuel_price

        total_fuel_liter += fuel_liter
        total_fuel_cost += fuel_cost

        delivered_weight = remaining_weight_by_destination.get(end, 0.0)
        current_weight -= delivered_weight

        details.append(
            {
                "from": start,
                "to": end,
                "distance": distance,
                "weight_before_delivery": current_weight + delivered_weight,
                "delivered_weight": delivered_weight,
                "fuel_liter": fuel_liter,
                "fuel_cost": fuel_cost,
            }
        )

    return {
        "fuel_liter": total_fuel_liter,
        "fuel_cost": total_fuel_cost,
        "details": details,
    }

def calculate_server_cost(execution_time_ms):
    return execution_time_ms * SERVER_COST_PER_MS

def calculate_tco(fuel_cost, execution_time_ms):
     
     server_cost = calculate_server_cost(execution_time_ms)
     return {
        "fuel_cost": fuel_cost,
        "server_cost": server_cost,
        "tco": fuel_cost + server_cost,
    }

