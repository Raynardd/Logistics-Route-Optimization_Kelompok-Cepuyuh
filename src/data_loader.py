import csv
from pathlib import Path

from utils import normalize_name, parse_decimal,validate_required_columns

def read_csv_rows(file_path):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {path}")
    
    with path.open("r", encoding="utf-8-sig",newline="") as file:
        return list(csv.DictReader(file))
    
def load_distance_edges(file_path):
    rows = read_csv_rows(file_path)

    if not rows:
        raise ValueError("data jarak kosong")
    
    validate_required_columns(file_path, rows[0],["Titik Awal","Titik Akhir", "Jarak", "Waktu Tempuh"])

    edges = []
    nodes = set()

    for row in rows:
        start = normalize_name(row["Titik Awal"])
        end = normalize_name(row["Titik Akhir"])
        distance = parse_decimal(row["Jarak"])
        travel_time = parse_decimal(row["Waktu Tempuh"])

        nodes.add(start)
        nodes.add(end)

        edges.append(
            {
                "start": start,
                "end": end,
                "distance": distance,
                "travel_time": travel_time,
            }
        )
    return sorted(nodes), edges

def load_vehicles(file_path):
    rows = read_csv_rows(file_path)

    if not rows:
        raise ValueError("Data kendaraan kosong.")

    validate_required_columns(
        file_path,
        rows[0],
        ["kendaraan", "jarak tempuh (per liter)", "kapasitas (kg)"],
    )

    vehicles = {}

    for row in rows:
        name = normalize_name(row["kendaraan"]).lower()
        vehicles[name] = {
            "name": name,
            "km_per_liter": parse_decimal(row["jarak tempuh (per liter)"]),
            "capacity_kg": parse_decimal(row["kapasitas (kg)"]),
        }

    return vehicles


def load_packages(file_path):
    rows = read_csv_rows(file_path)

    if not rows:
        raise ValueError("Data paket kosong.")

    validate_required_columns(
        file_path,
        rows[0],
        ["package_id", "package_name", "destination", "weight_kg"],
    )

    packages = []

    for row in rows:
        packages.append(
            {
                "package_id": row["package_id"],
                "package_name": row["package_name"],
                "destination": normalize_name(row["destination"]),
                "weight_kg": parse_decimal(row["weight_kg"]),
            }
        )

    return packages


def load_scenarios(file_path):
    rows = read_csv_rows(file_path)

    if not rows:
        raise ValueError("Data skenario kosong.")

    validate_required_columns(file_path, rows[0], ["skenario", "harga bbm"])

    scenarios = {}

    for row in rows:
        name = normalize_name(row["skenario"]).lower()
        scenarios[name] = {
            "name": name,
            "fuel_price": parse_decimal(row["harga bbm"]),
        }

    return scenarios


def load_project_data(data_dir, package_file_name):
    data_path = Path(data_dir)

    nodes, edges = load_distance_edges(data_path / "jarak_node.csv")
    vehicles = load_vehicles(data_path / "kendaraan.csv")
    packages = load_packages(data_path / package_file_name)
    scenarios = load_scenarios(data_path / "skenario.csv")

    return {
        "nodes": nodes,
        "edges": edges,
        "vehicles": vehicles,
        "packages": packages,
        "scenarios": scenarios,
    }


def validate_package_destinations(packages, graph_nodes):
    graph_node_set = set(graph_nodes)
    missing = sorted(
        {
            normalize_name(package["destination"])
            for package in packages
            if normalize_name(package["destination"]) not in graph_node_set
        }
    )

    if missing:
        raise ValueError(
            "Ada destination paket yang tidak ditemukan di data jarak: "
            + ", ".join(missing)
        )