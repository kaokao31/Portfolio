"""
AetherWeave 2.0 - Adaptive Overlay Network Demo
================================================
Features:
  - Node simulation with latency
  - Adaptive routing (Dijkstra)
  - Visual graph with matplotlib
  - Node failure + automatic reroute
  - Packet transmission simulation
"""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
import random
import time
import logging
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
# Data Structures
# ─────────────────────────────────────────
@dataclass
class Packet:
    source: str
    destination: str
    payload: str
    packet_id: int = field(default_factory=lambda: random.randint(1000, 9999))

    def __str__(self):
        return f"Packet[{self.packet_id}] {self.source} → {self.destination} | '{self.payload}'"


@dataclass
class Node:
    node_id: str
    alive: bool = True
    load: float = field(default_factory=lambda: random.uniform(0.1, 0.5))

    def fail(self):
        self.alive = False
        log.warning(f"💀 Node [{self.node_id}] has FAILED")

    def recover(self):
        self.alive = True
        log.info(f"✅ Node [{self.node_id}] has RECOVERED")


# ─────────────────────────────────────────
# AetherWeave Network
# ─────────────────────────────────────────
class AetherWeaveNetwork:
    def __init__(self):
        self.graph = nx.Graph()
        self.nodes: dict[str, Node] = {}
        self.packet_log = []

    def add_node(self, node_id: str):
        node = Node(node_id)
        self.nodes[node_id] = node
        self.graph.add_node(node_id)
        log.info(f"🟢 Node [{node_id}] added to network")

    def add_link(self, a: str, b: str, latency: float):
        self.graph.add_edge(a, b, weight=latency, latency=latency)
        log.info(f"🔗 Link [{a}] ↔ [{b}] | latency={latency}ms")

    def get_active_subgraph(self):
        """Return subgraph with only alive nodes"""
        alive_nodes = [n for n, obj in self.nodes.items() if obj.alive]
        return self.graph.subgraph(alive_nodes).copy()

    def find_route(self, src: str, dst: str) -> Optional[list]:
        subgraph = self.get_active_subgraph()
        try:
            path = nx.dijkstra_path(subgraph, src, dst, weight="weight")
            cost = nx.dijkstra_path_length(subgraph, src, dst, weight="weight")
            log.info(f"🛣️  Route found: {' → '.join(path)} | total latency={cost:.1f}ms")
            return path
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            log.error(f"❌ No route from [{src}] to [{dst}]")
            return None

    def send_packet(self, packet: Packet) -> bool:
        log.info(f"📤 Sending {packet}")
        path = self.find_route(packet.source, packet.destination)
        if path:
            log.info(f"✅ Packet delivered via: {' → '.join(path)}")
            self.packet_log.append({"packet": packet, "path": path, "success": True})
            return True
        else:
            log.error(f"💥 Packet DROPPED: {packet}")
            self.packet_log.append({"packet": packet, "path": None, "success": False})
            return False

    def fail_node(self, node_id: str):
        self.nodes[node_id].fail()

    def recover_node(self, node_id: str):
        self.nodes[node_id].recover()


# ─────────────────────────────────────────
# Visualization
# ─────────────────────────────────────────
def draw_network(net: AetherWeaveNetwork, highlight_path=None, title="AetherWeave 2.0 Network", ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 8))

    ax.clear()
    ax.set_facecolor("#0d1117")
    ax.figure.set_facecolor("#0d1117")

    G = net.graph
    pos = nx.spring_layout(G, seed=42, k=2)

    # Node colors
    node_colors = []
    for n in G.nodes():
        if not net.nodes[n].alive:
            node_colors.append("#ff4444")   # Red = dead
        elif highlight_path and n in highlight_path:
            node_colors.append("#00ffcc")   # Cyan = active path
        else:
            node_colors.append("#4488ff")   # Blue = normal

    # Edge colors & widths
    edge_colors = []
    edge_widths = []
    for u, v in G.edges():
        if highlight_path and len(highlight_path) > 1:
            path_edges = list(zip(highlight_path[:-1], highlight_path[1:]))
            if (u, v) in path_edges or (v, u) in path_edges:
                edge_colors.append("#00ffcc")
                edge_widths.append(4.0)
            else:
                edge_colors.append("#334466")
                edge_widths.append(1.0)
        else:
            edge_colors.append("#334466")
            edge_widths.append(1.5)

    # Draw edges
    nx.draw_networkx_edges(G, pos, ax=ax,
                           edge_color=edge_colors,
                           width=edge_widths,
                           alpha=0.8)

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, ax=ax,
                           node_color=node_colors,
                           node_size=800,
                           alpha=0.95)

    # Labels
    nx.draw_networkx_labels(G, pos, ax=ax,
                            font_color="white",
                            font_size=11,
                            font_weight="bold")

    # Edge latency labels
    edge_labels = {(u, v): f"{d['latency']}ms" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax,
                                 font_color="#aaaaaa",
                                 font_size=8,
                                 bbox=dict(alpha=0))

    # Legend
    legend = [
        mpatches.Patch(color="#4488ff", label="Active Node"),
        mpatches.Patch(color="#ff4444", label="Failed Node"),
        mpatches.Patch(color="#00ffcc", label="Active Route"),
    ]
    ax.legend(handles=legend, loc="upper left",
              facecolor="#1a2030", labelcolor="white", fontsize=9)

    ax.set_title(title, color="white", fontsize=14, fontweight="bold", pad=15)
    ax.axis("off")


# ─────────────────────────────────────────
# Build Demo Network
# ─────────────────────────────────────────
def build_demo_network() -> AetherWeaveNetwork:
    net = AetherWeaveNetwork()

    nodes = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta"]
    for n in nodes:
        net.add_node(n)

    links = [
        ("Alpha",   "Beta",    10),
        ("Alpha",   "Gamma",   25),
        ("Beta",    "Delta",   15),
        ("Beta",    "Gamma",   20),
        ("Gamma",   "Epsilon", 10),
        ("Delta",   "Epsilon", 12),
        ("Delta",   "Zeta",    30),
        ("Epsilon", "Zeta",    18),
        ("Epsilon", "Eta",     22),
        ("Zeta",    "Eta",     10),
    ]
    for a, b, lat in links:
        net.add_link(a, b, lat)

    return net


# ─────────────────────────────────────────
# Main Demo (Step-by-step with pause)
# ─────────────────────────────────────────
def run_demo():
    print("\n" + "="*55)
    print("  🌐 AetherWeave 2.0 — Adaptive Overlay Network Demo")
    print("="*55 + "\n")

    net = build_demo_network()

    fig, ax = plt.subplots(figsize=(13, 8))
    plt.ion()  # interactive mode

    # ── Step 1: Show initial network ──────────────────────
    print("📡 [Step 1] Initial Network\n")
    draw_network(net, title="Step 1: Initial Network — All Nodes Active", ax=ax)
    plt.tight_layout()
    plt.pause(0.1)
    input("  ▶ Press ENTER to send a packet...\n")

    # ── Step 2: Send packet Alpha → Eta ──────────────────
    print("📤 [Step 2] Sending Packet: Alpha → Eta\n")
    pkt1 = Packet("Alpha", "Eta", "Hello from Alpha!")
    path1 = net.find_route("Alpha", "Eta")
    net.send_packet(pkt1)

    draw_network(net, highlight_path=path1,
                 title=f"Step 2: Packet Routing — {' → '.join(path1) if path1 else 'No route'}",
                 ax=ax)
    plt.tight_layout()
    plt.pause(0.1)
    input("  ▶ Press ENTER to simulate node failure...\n")

    # ── Step 3: Node failure ──────────────────────────────
    failed_node = "Epsilon"
    print(f"💥 [Step 3] Simulating Failure: Node [{failed_node}]\n")
    net.fail_node(failed_node)

    draw_network(net, title=f"Step 3: Node [{failed_node}] FAILED — Network Disrupted", ax=ax)
    plt.tight_layout()
    plt.pause(0.1)
    input("  ▶ Press ENTER to reroute...\n")

    # ── Step 4: Reroute ───────────────────────────────────
    print("🔄 [Step 4] Adaptive Reroute: Alpha → Eta\n")
    pkt2 = Packet("Alpha", "Eta", "Rerouted packet!")
    path2 = net.find_route("Alpha", "Eta")
    net.send_packet(pkt2)

    if path2:
        draw_network(net, highlight_path=path2,
                     title=f"Step 4: REROUTED — {' → '.join(path2)}",
                     ax=ax)
    else:
        draw_network(net, title="Step 4: ❌ No Route Available!", ax=ax)
    plt.tight_layout()
    plt.pause(0.1)
    input("  ▶ Press ENTER to recover node...\n")

    # ── Step 5: Recovery ─────────────────────────────────
    print(f"✅ [Step 5] Node [{failed_node}] Recovering...\n")
    net.recover_node(failed_node)

    path3 = net.find_route("Alpha", "Eta")
    draw_network(net, highlight_path=path3,
                 title=f"Step 5: Node [{failed_node}] RECOVERED — Optimal Route Restored",
                 ax=ax)
    plt.tight_layout()
    plt.pause(0.1)
    input("  ▶ Press ENTER to see summary...\n")

    # ── Step 6: Summary ───────────────────────────────────
    print("\n" + "="*55)
    print("  📊 DEMO SUMMARY")
    print("="*55)
    for i, entry in enumerate(net.packet_log, 1):
        p = entry["packet"]
        status = "✅ Delivered" if entry["success"] else "❌ Dropped"
        path_str = " → ".join(entry["path"]) if entry["path"] else "N/A"
        print(f"  [{i}] {p.payload}")
        print(f"       Route : {path_str}")
        print(f"       Status: {status}\n")
    print("="*55)

    plt.ioff()
    draw_network(net, highlight_path=path3,
                 title="AetherWeave 2.0 — Demo Complete ✅",
                 ax=ax)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    run_demo()
