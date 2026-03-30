"""
AetherWeave 2.0 - Reliable Path Simulation
===========================================
เปรียบเทียบ 2 โหมด:
  - Shortest Path  : เลือกเส้นทางที่ Latency รวมน้อยที่สุด
  - Reliable Path  : เลือกเส้นทางที่น่าเชื่อถือที่สุด
                     (คำนึงถึง Latency + Reliability Score + Packet Loss)

Reliability Score ของแต่ละ Node:
  - 1.0 = เสถียรมาก (ไม่ค่อยล่ม)
  - 0.5 = เสถียรปานกลาง
  - 0.0 = ล่มบ่อย / ไม่น่าเชื่อถือ

Edge Weight สำหรับ Reliable Path:
  weight = latency / (reliability_src * reliability_dst)
  → เส้นทางที่ผ่าน Node ไม่น่าเชื่อถือจะมี weight สูงขึ้น
  → ระบบจะหลีกเลี่ยงเส้นทางนั้นแม้ Latency จะต่ำกว่า
"""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import logging
import random
from dataclasses import dataclass, field
from typing import Optional

# ─────────────────────────────────────────
# Logging
# ─────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger("AetherWeave")

# ─────────────────────────────────────────
# Node
# ─────────────────────────────────────────
@dataclass
class Node:
    node_id: str
    reliability: float  # 0.0 - 1.0 (1.0 = เสถียรที่สุด)
    alive: bool = True

    def reliability_label(self):
        if self.reliability >= 0.85:
            return "HIGH"
        elif self.reliability >= 0.6:
            return "MED"
        else:
            return "LOW"

# ─────────────────────────────────────────
# Packet
# ─────────────────────────────────────────
@dataclass
class Packet:
    source: str
    destination: str
    payload: str
    packet_id: int = field(default_factory=lambda: random.randint(1000, 9999))

# ─────────────────────────────────────────
# Network
# ─────────────────────────────────────────
class AetherWeaveNetwork:
    def __init__(self):
        self.graph = nx.Graph()
        self.nodes: dict[str, Node] = {}

    def add_node(self, node_id: str, reliability: float):
        node = Node(node_id, reliability)
        self.nodes[node_id] = node
        self.graph.add_node(node_id, reliability=reliability)
        log.info(f"🟢 Node [{node_id}] | Reliability={reliability:.0%} ({node.reliability_label()})")

    def add_link(self, a: str, b: str, latency: float, packet_loss: float = 0.0):
        """
        packet_loss: 0.0 - 1.0 (โอกาสที่ packet จะหายบนเส้นนี้)
        """
        self.graph.add_edge(a, b, latency=latency, packet_loss=packet_loss)
        log.info(f"🔗 Link [{a}] ↔ [{b}] | latency={latency}ms | loss={packet_loss:.0%}")

    def _shortest_weight(self, u, v, data):
        """Weight สำหรับ Shortest Path = Latency อย่างเดียว"""
        return data["latency"]

    def _reliable_weight(self, u, v, data):
        """
        Weight สำหรับ Reliable Path
        = latency / (reliability_u * reliability_v) + penalty จาก packet_loss
        → Node ที่ไม่น่าเชื่อถือจะทำให้ weight สูงขึ้น
        """
        rel_u = self.nodes[u].reliability
        rel_v = self.nodes[v].reliability
        combined_reliability = rel_u * rel_v
        if combined_reliability == 0:
            return float("inf")
        loss_penalty = data.get("packet_loss", 0) * 100
        return (data["latency"] / combined_reliability) + loss_penalty

    def find_shortest_path(self, src: str, dst: str):
        try:
            path = nx.dijkstra_path(self.graph, src, dst, weight=self._shortest_weight)
            cost = nx.dijkstra_path_length(self.graph, src, dst, weight=self._shortest_weight)
            log.info(f"📍 [SHORTEST] {' → '.join(path)} | latency={cost:.1f}ms")
            return path, cost
        except Exception:
            log.error(f"❌ No shortest path from [{src}] to [{dst}]")
            return None, None

    def find_reliable_path(self, src: str, dst: str):
        try:
            path = nx.dijkstra_path(self.graph, src, dst, weight=self._reliable_weight)
            # คำนวณ latency จริงของเส้นทางนี้
            latency = sum(
                self.graph[path[i]][path[i+1]]["latency"]
                for i in range(len(path)-1)
            )
            # คำนวณ reliability รวม
            reliability = 1.0
            for node_id in path:
                reliability *= self.nodes[node_id].reliability
            log.info(f"🛡️  [RELIABLE] {' → '.join(path)} | latency={latency:.1f}ms | reliability={reliability:.0%}")
            return path, latency, reliability
        except Exception:
            log.error(f"❌ No reliable path from [{src}] to [{dst}]")
            return None, None, None

# ─────────────────────────────────────────
# Visualization
# ─────────────────────────────────────────
def draw_comparison(net: AetherWeaveNetwork,
                    shortest_path: list,
                    reliable_path: list,
                    src: str, dst: str):
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))
    fig.patch.set_facecolor("#0d1117")
    fig.suptitle(
        f"AetherWeave 2.0 — Path Comparison: {src} → {dst}",
        color="white", fontsize=16, fontweight="bold", y=0.98
    )

    G = net.graph
    pos = nx.spring_layout(G, seed=42, k=2.2)

    titles = ["🔵 Shortest Path\n(ตาม Latency น้อยสุด)",
              "🛡️  Reliable Path\n(ตาม Reliability สูงสุด)"]
    paths = [shortest_path, reliable_path]
    path_colors = ["#00aaff", "#00ffcc"]

    for ax, title, path, path_color in zip(axes, titles, paths, path_colors):
        ax.set_facecolor("#0d1117")
        ax.set_title(title, color="white", fontsize=13, fontweight="bold", pad=12)

        # Node colors ตาม reliability
        node_colors = []
        node_sizes = []
        for n in G.nodes():
            rel = net.nodes[n].reliability
            if path and n in path:
                node_colors.append(path_color)
                node_sizes.append(900)
            elif rel >= 0.85:
                node_colors.append("#4488ff")   # สีน้ำเงิน = น่าเชื่อถือ
                node_sizes.append(700)
            elif rel >= 0.6:
                node_colors.append("#ffaa00")   # สีส้ม = ปานกลาง
                node_sizes.append(700)
            else:
                node_colors.append("#ff4444")   # สีแดง = ไม่น่าเชื่อถือ
                node_sizes.append(700)

        # Edge colors
        edge_colors = []
        edge_widths = []
        for u, v in G.edges():
            if path and len(path) > 1:
                path_edges = list(zip(path[:-1], path[1:]))
                if (u, v) in path_edges or (v, u) in path_edges:
                    edge_colors.append(path_color)
                    edge_widths.append(4.0)
                else:
                    edge_colors.append("#334466")
                    edge_widths.append(1.0)
            else:
                edge_colors.append("#334466")
                edge_widths.append(1.5)

        nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors,
                               width=edge_widths, alpha=0.85)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors,
                               node_size=node_sizes, alpha=0.95)
        nx.draw_networkx_labels(G, pos, ax=ax, font_color="white",
                                font_size=10, font_weight="bold")

        # Edge labels: latency + loss
        edge_labels = {}
        for u, v, d in G.edges(data=True):
            loss = d.get("packet_loss", 0)
            label = f"{d['latency']}ms"
            if loss > 0:
                label += f"\n⚠️{loss:.0%}loss"
            edge_labels[(u, v)] = label
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax,
                                     font_color="#aaaaaa", font_size=7,
                                     bbox=dict(alpha=0))

        # Node reliability labels
        rel_labels = {n: f"{net.nodes[n].reliability:.0%}" for n in G.nodes()}
        offset_pos = {n: (p[0], p[1] - 0.18) for n, p in pos.items()}
        nx.draw_networkx_labels(G, offset_pos, labels=rel_labels, ax=ax,
                                font_color="#aaaacc", font_size=8)

        # Path info box
        if path:
            path_str = " → ".join(path)
            latency = sum(G[path[i]][path[i+1]]["latency"] for i in range(len(path)-1))
            rel = 1.0
            for n in path:
                rel *= net.nodes[n].reliability
            info = f"Route: {path_str}\nLatency: {latency}ms | Reliability: {rel:.0%}"
        else:
            info = "❌ No path found"

        ax.text(0.5, 0.02, info, transform=ax.transAxes,
                color="white", fontsize=9, ha="center",
                bbox=dict(boxstyle="round,pad=0.4", facecolor="#1a2535", alpha=0.85))

        ax.axis("off")

    # Legend
    legend_elements = [
        mpatches.Patch(color="#4488ff", label="Reliability HIGH (≥85%)"),
        mpatches.Patch(color="#ffaa00", label="Reliability MED (60-84%)"),
        mpatches.Patch(color="#ff4444", label="Reliability LOW (<60%)"),
        mpatches.Patch(color="#00aaff", label="Shortest Path"),
        mpatches.Patch(color="#00ffcc", label="Reliable Path"),
    ]
    fig.legend(handles=legend_elements, loc="lower center", ncol=5,
               facecolor="#1a2535", labelcolor="white", fontsize=9,
               framealpha=0.9, bbox_to_anchor=(0.5, 0.01))

    plt.tight_layout(rect=[0, 0.06, 1, 0.96])


# ─────────────────────────────────────────
# Build Network
# ─────────────────────────────────────────
def build_network() -> AetherWeaveNetwork:
    net = AetherWeaveNetwork()

    # Node: (node_id, reliability)
    # Epsilon และ Beta จงใจให้ reliability ต่ำ
    # เพื่อให้เห็นชัดว่า Reliable Path หลีกเลี่ยงพวกนี้
    nodes = [
        ("Alpha",   1.0),   # เสถียรมาก
        ("Beta",    0.5),   # ปานกลาง
        ("Gamma",   0.9),   # เสถียรมาก
        ("Delta",   0.85),  # เสถียรมาก
        ("Epsilon", 0.4),   # ไม่ค่อยน่าเชื่อถือ ⚠️
        ("Zeta",    0.95),  # เสถียรมาก
        ("Eta",     1.0),   # เสถียรมาก
    ]
    for node_id, rel in nodes:
        net.add_node(node_id, rel)

    # Link: (a, b, latency, packet_loss)
    links = [
        ("Alpha",   "Beta",    10,  0.20),  # Latency ต่ำ แต่ loss สูง ⚠️
        ("Alpha",   "Gamma",   25,  0.0),
        ("Beta",    "Delta",   15,  0.15),
        ("Beta",    "Gamma",   20,  0.10),
        ("Gamma",   "Epsilon", 10,  0.0),
        ("Delta",   "Epsilon", 12,  0.0),
        ("Delta",   "Zeta",    30,  0.0),
        ("Epsilon", "Zeta",    18,  0.0),
        ("Epsilon", "Eta",     22,  0.0),
        ("Zeta",    "Eta",     10,  0.0),
    ]
    for a, b, lat, loss in links:
        net.add_link(a, b, lat, loss)

    return net


# ─────────────────────────────────────────
# Main Demo
# ─────────────────────────────────────────
def run_demo():
    print("\n" + "="*60)
    print("  🌐 AetherWeave 2.0 — Shortest vs Reliable Path Demo")
    print("="*60)

    net = build_network()

    # รับ Input จาก User
    print("\n📋 Node ที่มีในระบบ:")
    for nid, node in net.nodes.items():
        print(f"   {nid:10s} | Reliability: {node.reliability:.0%} ({node.reliability_label()})")

    print()
    src = input("  ➤ ใส่ Source Node      : ").strip().capitalize()
    dst = input("  ➤ ใส่ Destination Node : ").strip().capitalize()

    if src not in net.nodes or dst not in net.nodes:
        print(f"\n❌ ไม่พบ Node '{src}' หรือ '{dst}' ในระบบครับ")
        return

    print(f"\n🔍 กำลังหาเส้นทาง {src} → {dst}...\n")

    # หาเส้นทาง
    shortest_path, shortest_cost = net.find_shortest_path(src, dst)
    reliable_path, reliable_latency, reliable_score = net.find_reliable_path(src, dst)

    # สรุปผล
    print("\n" + "="*60)
    print("  📊 ผลการเปรียบเทียบ")
    print("="*60)

    if shortest_path:
        print(f"\n  🔵 Shortest Path  : {' → '.join(shortest_path)}")
        print(f"     Latency        : {shortest_cost:.1f} ms")
        rel = 1.0
        for n in shortest_path:
            rel *= net.nodes[n].reliability
        print(f"     Reliability    : {rel:.0%}")

    if reliable_path:
        print(f"\n  🛡️  Reliable Path  : {' → '.join(reliable_path)}")
        print(f"     Latency        : {reliable_latency:.1f} ms")
        print(f"     Reliability    : {reliable_score:.0%}")

    if shortest_path and reliable_path:
        if shortest_path == reliable_path:
            print("\n  ✅ ทั้งสองเส้นทางเหมือนกัน — เส้นนี้ดีทั้ง Latency และ Reliability!")
        else:
            print(f"\n  ⚡ Shortest เร็วกว่า {reliable_latency - shortest_cost:.1f}ms")
            print(f"  🛡️  Reliable น่าเชื่อถือกว่า — หลีกเลี่ยง Node/Link ที่ไม่เสถียร")

    print("="*60)

    # แสดงกราฟ
    draw_comparison(net, shortest_path, reliable_path, src, dst)
    plt.show()


if __name__ == "__main__":
    run_demo()
