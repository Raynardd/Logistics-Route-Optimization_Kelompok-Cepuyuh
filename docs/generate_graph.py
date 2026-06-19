"""
Script: generate_graph.py
Jalankan dari root repo: python generate_graph.py
Requires: pip install matplotlib
Output: docs/graph_visualization.png
"""

import csv
import math
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def parse_decimal(value):
    return float(str(value).strip().replace(".", "").replace(",", "."))


def normalize(value):
    return " ".join(str(value).strip().split())


# 1. Baca CSV
edges_raw = []
nodes = set()

with open("data/jarak_node.csv", encoding="utf-8-sig", newline="") as f:
    for row in csv.DictReader(f):
        a = normalize(row["Titik Awal"])
        b = normalize(row["Titik Akhir"])
        d = parse_decimal(row["Jarak"])
        if a == b or d == 0:
            continue
        nodes.add(a)
        nodes.add(b)
        edges_raw.append((a, b, d))

nodes = sorted(nodes)
HUB = "JNE Sukamanah"

# 2. Spring layout
random.seed(42)
pos = {n: [random.uniform(-1, 1), random.uniform(-1, 1)] for n in nodes}
pos[HUB] = [0.0, 0.0]


def spring_layout(pos, edges, iterations=300, k=0.6, repulsion=0.4):
    node_list = list(pos.keys())
    for _ in range(iterations):
        force = {n: [0.0, 0.0] for n in node_list}
        for i, u in enumerate(node_list):
            for v in node_list[i + 1:]:
                dx = pos[u][0] - pos[v][0]
                dy = pos[u][1] - pos[v][1]
                dist = max(math.hypot(dx, dy), 0.01)
                f = repulsion / dist ** 2
                force[u][0] += f * dx / dist
                force[u][1] += f * dy / dist
                force[v][0] -= f * dx / dist
                force[v][1] -= f * dy / dist
        for a, b, w in edges:
            dx = pos[a][0] - pos[b][0]
            dy = pos[a][1] - pos[b][1]
            dist = max(math.hypot(dx, dy), 0.01)
            ideal = k * (1 / w)
            f = (dist - ideal) * 0.05
            force[a][0] -= f * dx / dist
            force[a][1] -= f * dy / dist
            force[b][0] += f * dx / dist
            force[b][1] += f * dy / dist
        for n in node_list:
            if n == HUB:
                continue
            pos[n][0] += force[n][0] * 0.1
            pos[n][1] += force[n][1] * 0.1
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    span = max(max_x - min_x, max_y - min_y, 0.001)
    for n in pos:
        pos[n][0] = (pos[n][0] - min_x) / span * 2 - 1
        pos[n][1] = (pos[n][1] - min_y) / span * 2 - 1
    return pos


pos = spring_layout(pos, edges_raw)

# 3. Gambar — background PUTIH
fig, ax = plt.subplots(figsize=(16, 12), facecolor="white")
ax.set_facecolor("white")

C_HUB   = "#dc2626"   # merah
C_NODE  = "#2563eb"   # biru
C_EDGE  = "#9ca3af"   # abu-abu
C_ELBL  = "#6b7280"   # abu-abu gelap
C_TEXT  = "#111827"   # hitam

drawn = set()
for a, b, dist in sorted(edges_raw, key=lambda x: x[2]):
    key = tuple(sorted([a, b]))
    if key in drawn:
        continue
    drawn.add(key)
    x1, y1 = pos[a]
    x2, y2 = pos[b]
    ax.plot([x1, x2], [y1, y2], color=C_EDGE, linewidth=0.9, alpha=0.7, zorder=1)
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    ax.text(mid_x, mid_y, f"{dist:.2f} km",
            fontsize=5.5, color=C_ELBL, ha="center", va="center",
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.8, pad=0.4),
            zorder=3)

for n in nodes:
    x, y = pos[n]
    is_hub = (n == HUB)
    color  = C_HUB if is_hub else C_NODE
    size   = 240 if is_hub else 140
    ax.scatter(x, y, s=size, c=color, zorder=5,
               edgecolors="white", linewidths=1.2)
    offset_y = 0.07 if is_hub else 0.055
    ax.text(x, y + offset_y, n,
            fontsize=8.5 if is_hub else 7.5,
            color=C_TEXT, ha="center", va="bottom",
            fontweight="bold" if is_hub else "normal",
            bbox=dict(facecolor="white", edgecolor="#e5e7eb", alpha=0.9,
                      pad=1.5, boxstyle="round,pad=0.3"),
            zorder=6)

hub_patch  = mpatches.Patch(color=C_HUB,  label="Hub (JNE Sukamanah)")
node_patch = mpatches.Patch(color=C_NODE, label="Lokasi Pelanggan (12 titik)")
ax.legend(handles=[hub_patch, node_patch], loc="lower right", fontsize=9,
          facecolor="white", edgecolor="#d1d5db")

ax.set_title("Graf Berbobot — Jaringan Rute Last-Mile Delivery\nKelompok Cepuyuh | Jatinangor",
             fontsize=14, color=C_TEXT, pad=16, fontweight="bold")
ax.axis("off")
plt.tight_layout(pad=1.5)

output = "docs/graph_visualization.png"
plt.savefig(output, dpi=180, bbox_inches="tight", facecolor="white")
print("Saved:", output)
plt.close()
