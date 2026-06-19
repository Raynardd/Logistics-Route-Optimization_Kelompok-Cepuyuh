import sys
from data_loader import load_project_data
from graph import build_graph
from greedy import run_greedy
from held_karp import held_karp
from cost import calculate_route_fuel_cost, calculate_server_cost
from utils import measure_time_ms, format_rupiah, format_route

def main():
    while True:
        print("\n" + "="*45)
        print("MENU SIMULASI OPTIMASI RUTE LOGISTIK")
        print("="*45)
        print("Pilih Skenario BBM:")
        print("1. Skenario Subsidi  (Rp 5.000/liter)")
        print("2. Skenario Krisis   (Rp 20.000/liter)")
        print("3. Bandingkan Kedua Skenario")
        print("0. Keluar")
        
        pilihan_skenario = input("Masukkan pilihan (1/2/3/0): ")
        
        if pilihan_skenario == '0':
            print("Keluar dari program")
            break
        
        selected_scenarios = []
        if pilihan_skenario == '1':
            selected_scenarios = ["subsidi"]
        elif pilihan_skenario == '2':
            selected_scenarios = ["krisis"]
        elif pilihan_skenario == '3':
            selected_scenarios = ["subsidi", "krisis"]
        else:
            print("Pilihan tidak valid")
            continue

        print("\nPilih Paket:")
        print("1. Paket 50kg")
        print("2. Paket 75kg")
        print("3. Paket 200kg")
        
        pilihan_paket = input("Masukkan pilihan paket (1/2/3): ")
        
        if pilihan_paket == '1':
            package_file = "paket_50kg.csv"
            vehicle_key = "beat"
        elif pilihan_paket == '2':
            package_file = "paket_75kg.csv"
            vehicle_key = "nmax"
        elif pilihan_paket == '3':
            package_file = "paket_200kg.csv"
            vehicle_key = "pick-up"
        else:
            print("Pilihan tidak valid")
            continue

        data = load_project_data("data", package_file)
        graph = build_graph([n for n in data["nodes"]], data["edges"])
        hub = "JNE Sukamanah"
        destinations = [p["destination"] for p in data["packages"]]
        vehicle = data["vehicles"][vehicle_key]

        for scenario in selected_scenarios:
            print(f"\n{'='*65}")
            print(f"--- Memulai Simulasi: Skenario {scenario.upper()} dengan {package_file} ---")
            print(f"{'='*65}")
            
            fuel_price = data["scenarios"][scenario]["fuel_price"]

            greedy_res, t_greedy = measure_time_ms(run_greedy, graph, hub, data["packages"])
            cost_greedy = calculate_route_fuel_cost(graph, greedy_res["route"], data["packages"], vehicle, fuel_price)
            server_cost_greedy = calculate_server_cost(t_greedy) 
            tco_greedy = cost_greedy["fuel_cost"] + server_cost_greedy

            dest_unique = list(set(destinations))
            hk_result, t_hk = measure_time_ms(held_karp, graph, hub, dest_unique)
            hk_path = hk_result[0]
            cost_hk = calculate_route_fuel_cost(graph, hk_path, data["packages"], vehicle, fuel_price)
            server_cost_hk = calculate_server_cost(t_hk) 
            tco_hk = cost_hk["fuel_cost"] + server_cost_hk

            print(f"\n[GREEDY ALGORITHM - HEURISTIK]")
            print(f"Waktu Komputasi: {t_greedy:.2f} ms")
            print(f"├─ Biaya Server : {format_rupiah(server_cost_greedy)}")
            print(f"├─ Biaya BBM    : {format_rupiah(cost_greedy['fuel_cost'])}")
            print(f"└─ Total (TCO)  : {format_rupiah(tco_greedy)}")
            print(f"Rute: {format_route(greedy_res['route'])}")
            
            print(f"\n[HELD-KARP ALGORITHM - EKSAK]")
            print(f"Waktu Komputasi: {t_hk:.2f} ms")
            print(f"├─ Biaya Server : {format_rupiah(server_cost_hk)}")
            print(f"├─ Biaya BBM    : {format_rupiah(cost_hk['fuel_cost'])}")
            print(f"└─ Total (TCO)  : {format_rupiah(tco_hk)}")
            print(f"Rute: {format_route(hk_path)}")
            
        input("\nTekan Enter untuk kembali ke menu")

if __name__ == "__main__":
    main()