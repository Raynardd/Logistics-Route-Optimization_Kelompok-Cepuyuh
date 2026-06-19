"""
Script: generate_tco_chart.py
Jalankan dari root repo: python generate_tco_chart.py
Requires: pip install matplotlib
Output: docs/tco_comparison.png
"""

import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

sys.path.insert(0, "src")

from data_loader import load_project_data
from graph import build_graph
from greedy import run_greedy
from held_karp import held_karp
from cost import calculate_route_fuel_cost, calculate_server_cost
from utils import measure_time_ms

# 1. Simulasi
CONFIGS = [
    ("paket_50kg.csv",  "beat",    "Beat\n50 kg"),
    ("paket_75kg.csv",  "nmax",    "NMax\n75 kg"),
    ("paket_200kg.csv", "pick-up", "Pick-up\n200 kg"),
]
SCENARIOS = [
    ("subsidi", "Subsidi\n(Rp 5.000/L)"),
    ("krisis",  "Krisis\n(Rp 20.000/L)"),
]

results = []
times_g_per_veh  = []
times_hk_per_veh = []

for pkg_file, veh_key, veh_label in CONFIGS:
    data    = load_project_data("data", pkg_file)
    graph   = build_graph(list(data["nodes"]), data["edges"])
    hub     = "JNE Sukamanah"
    pkgs    = data["packages"]
    vehicle = data["vehicles"][veh_key]

    greedy_res, t_g = measure_time_ms(run_greedy, graph, hub, pkgs)
    dest_unique      = list(set(p["destination"] for p in pkgs))
    hk_res, t_hk    = measure_time_ms(held_karp, graph, hub, dest_unique)
    hk_path          = hk_res[0]

    times_g_per_veh.append(t_g)
    times_hk_per_veh.append(t_hk)

    sc_g  = calculate_server_cost(t_g)
    sc_hk = calculate_server_cost(t_hk)

    for sc_key, sc_label in SCENARIOS:
        fuel_price = data["scenarios"][sc_key]["fuel_price"]
        cost_g  = calculate_route_fuel_cost(graph, greedy_res["route"], pkgs, vehicle, fuel_price)
        cost_hk = calculate_route_fuel_cost(graph, hk_path,             pkgs, vehicle, fuel_price)
        results.append({
            "veh": veh_label,
            "sc": sc_label,
            "sc_key": sc_key,
            "tco_g":  cost_g["fuel_cost"]  + sc_g,
            "tco_hk": cost_hk["fuel_cost"] + sc_hk,
            "bbm_g":  cost_g["fuel_cost"],
            "bbm_hk": cost_hk["fuel_cost"],
            "srv_g":  sc_g,
            "srv_hk": sc_hk,
        })

# 2. Warna & layout
C_GREEDY = "#16a34a"   # hijau
C_HK     = "#2563eb"   # biru
C_GRID   = "#e5e7eb"
C_TEXT   = "#111827"
C_SUB    = "#6b7280"
C_ANNOT  = "#374151"

fig = plt.figure(figsize=(20, 9), facecolor="white")
fig.patch.set_facecolor("white")

# Subplot layout: [TCO bars | execution time]
gs = fig.add_gridspec(1, 2, width_ratios=[3, 1], wspace=0.08)
ax_tco  = fig.add_subplot(gs[0])
ax_time = fig.add_subplot(gs[1])

for ax in [ax_tco, ax_time]:
    ax.set_facecolor("white")

# 3. TCO grouped bar chart (non-stacked, total TCO)
n = len(results)
x = list(range(n))
bar_w = 0.35

bars_g  = ax_tco.bar([v - bar_w/2 for v in x], [r["tco_g"]  for r in results],
                     width=bar_w, color=C_GREEDY, label="Greedy (Heuristik)", zorder=3,
                     edgecolor="white", linewidth=0.5)
bars_hk = ax_tco.bar([v + bar_w/2 for v in x], [r["tco_hk"] for r in results],
                     width=bar_w, color=C_HK,     label="Held-Karp (Eksak)",   zorder=3,
                     edgecolor="white", linewidth=0.5)

# Annotasi nilai TCO di atas bar
max_val = max(r["tco_hk"] for r in results)
for bar, r in zip(bars_g, results):
    h = bar.get_height()
    ax_tco.text(bar.get_x() + bar.get_width()/2, h + max_val * 0.008,
                f"Rp {h:,.0f}", ha="center", va="bottom",
                fontsize=7, color=C_GREEDY, fontweight="bold")

for bar, r in zip(bars_hk, results):
    h = bar.get_height()
    ax_tco.text(bar.get_x() + bar.get_width()/2, h + max_val * 0.008,
                f"Rp {h:,.0f}", ha="center", va="bottom",
                fontsize=7, color=C_HK, fontweight="bold")

# Garis pemisah antar kendaraan
for sep in [1.5, 3.5]:
    ax_tco.axvline(sep, color=C_GRID, linewidth=1.5, linestyle="--", zorder=2)

# Label grup kendaraan di bagian atas
veh_names = ["Motor Beat (50 kg)", "Motor NMax (75 kg)", "Pick-up (200 kg)"]
ylim_top = max_val * 1.18
for i, name in enumerate(veh_names):
    ax_tco.text(i * 2 + 0.5, ylim_top * 0.97, name,
                ha="center", va="top", fontsize=9, color=C_SUB, fontstyle="italic")

# Sumbu
labels_x = [f"{r['sc']}" for r in results]
ax_tco.set_xticks(x)
ax_tco.set_xticklabels(labels_x, fontsize=8, color=C_TEXT)
ax_tco.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"Rp {v:,.0f}"))
ax_tco.tick_params(axis="y", colors=C_SUB, labelsize=8)
ax_tco.set_ylim(0, ylim_top)

for spine in ["top", "right"]:
    ax_tco.spines[spine].set_visible(False)
ax_tco.spines["left"].set_color(C_GRID)
ax_tco.spines["bottom"].set_color(C_GRID)
ax_tco.yaxis.grid(True, color=C_GRID, linewidth=0.7)
ax_tco.set_axisbelow(True)

ax_tco.set_ylabel("Total Cost of Ownership (TCO)", color=C_SUB, fontsize=10)
ax_tco.set_title("Perbandingan TCO: Greedy vs Held-Karp\nper Kendaraan & Skenario BBM",
                 color=C_TEXT, fontsize=13, fontweight="bold", pad=14)
ax_tco.legend(loc="upper left", fontsize=9, framealpha=0.9,
              edgecolor=C_GRID, facecolor="white")

# 4. Execution time — horizontal bar
veh_labels_short = ["Beat 50kg", "NMax 75kg", "Pick-up 200kg"]
y = list(range(3))
bar_h = 0.35

ax_time.barh([v + bar_h/2 for v in y], times_g_per_veh,
             height=bar_h, color=C_GREEDY, label="Greedy", zorder=3,
             edgecolor="white")
ax_time.barh([v - bar_h/2 for v in y], times_hk_per_veh,
             height=bar_h, color=C_HK,     label="Held-Karp", zorder=3,
             edgecolor="white")

max_t = max(times_hk_per_veh)
for v, t in zip([v + bar_h/2 for v in y], times_g_per_veh):
    ax_time.text(t + max_t * 0.02, v, f"{t:.2f} ms",
                 va="center", fontsize=8, color=C_GREEDY, fontweight="bold")
for v, t in zip([v - bar_h/2 for v in y], times_hk_per_veh):
    ax_time.text(t + max_t * 0.02, v, f"{t:.2f} ms",
                 va="center", fontsize=8, color=C_HK, fontweight="bold")

ax_time.set_yticks(y)
ax_time.set_yticklabels(veh_labels_short, fontsize=9, color=C_TEXT)
ax_time.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.0f} ms"))
ax_time.tick_params(axis="x", colors=C_SUB, labelsize=8)
ax_time.set_xlim(0, max_t * 1.3)

for spine in ["top", "right"]:
    ax_time.spines[spine].set_visible(False)
ax_time.spines["left"].set_color(C_GRID)
ax_time.spines["bottom"].set_color(C_GRID)
ax_time.xaxis.grid(True, color=C_GRID, linewidth=0.7)
ax_time.set_axisbelow(True)

ax_time.set_xlabel("Waktu Eksekusi (ms)", color=C_SUB, fontsize=10)
ax_time.set_title("Kecepatan\nKomputasi", color=C_TEXT, fontsize=13,
                  fontweight="bold", pad=14)
ax_time.legend(fontsize=9, framealpha=0.9, edgecolor=C_GRID, facecolor="white")

# 5. Caption bawah
fig.text(0.5, 0.005,
         "TCO = Biaya BBM + Biaya Server Komputasi  |  "
         "Biaya Server = Waktu Eksekusi x Rp 50/ms  |  "
         "Greedy: total rute 6,51 km  |  Held-Karp: rute optimal 5,51 km",
         ha="center", color=C_SUB, fontsize=8)

plt.tight_layout(rect=[0, 0.04, 1, 1])

output = "docs/tco_comparison.png"
plt.savefig(output, dpi=180, bbox_inches="tight", facecolor="white")
print("Saved:", output)
plt.close()
