import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# Union-Find structure for cycle detection
class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, p):
        if self.parent[p] != p:
            self.parent[p] = self.find(self.parent[p])
        return self.parent[p]

    def union(self, p, q):
        rootP = self.find(p)
        rootQ = self.find(q)
        if rootP == rootQ:
            return False
        if self.rank[rootP] < self.rank[rootQ]:
            self.parent[rootP] = rootQ
        elif self.rank[rootP] > self.rank[rootQ]:
            self.parent[rootQ] = rootP
        else:
            self.parent[rootQ] = rootP
            self.rank[rootP] += 1
        return True

# Kruskal's algorithm with steps for animation
def kruskal_mst(graph):
    edges = sorted(graph.edges(data=True), key=lambda x: x[2]['weight'])
    uf = UnionFind(len(graph.nodes))
    mst_edges = []
    steps = []  # List of (edge, added) for animation

    for u, v, data in edges:
        if uf.union(u, v):
            steps.append(((u, v), True))  # Added to MST
            mst_edges.append((u, v, data))
        else:
            steps.append(((u, v), False))  # Skipped (cycle)

    return mst_edges, steps

# Generate random graph
def generate_random_graph(num_nodes=10, edge_prob=0.3):
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < edge_prob:
                weight = random.randint(1, 20)
                G.add_edge(i, j, weight=weight)
    return G

# Visualization function
def visualize_mst_animation(graph, steps):
    pos = nx.spring_layout(graph)  # Fixed layout
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_title("Real-Time MST Construction (Kruskal's Algorithm)")

    # Initial draw: nodes and all edges in gray
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_color='lightblue', node_size=500)
    nx.draw_networkx_labels(graph, pos, ax=ax)
    nx.draw_networkx_edges(graph, pos, ax=ax, edge_color='gray', width=1)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels={(u, v): d['weight'] for u, v, d in graph.edges(data=True)}, ax=ax)

    # Track added edges for color update
    added_edges = []

    def update(frame):
        ax.clear()
        ax.set_title(f"Step {frame + 1}: Processing edges...")
        
        # Redraw nodes and labels
        nx.draw_networkx_nodes(graph, pos, ax=ax, node_color='lightblue', node_size=500)
        nx.draw_networkx_labels(graph, pos, ax=ax)
        
        # Draw all edges: gray for untouched, green for added, red for skipped
        edge_colors = []
        for u, v in graph.edges():
            if (u, v) in added_edges or (v, u) in added_edges:
                edge_colors.append('green')
            elif frame < len(steps) and ((u, v) == steps[frame][0] or (v, u) == steps[frame][0]):
                # Current edge being processed
                edge_colors.append('blue' if steps[frame][1] else 'orange')
            else:
                edge_colors.append('gray')
        
        nx.draw_networkx_edges(graph, pos, ax=ax, edge_color=edge_colors, width=2)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels={(u, v): d['weight'] for u, v, d in graph.edges(data=True)}, ax=ax)

        if frame < len(steps):
            edge, added = steps[frame]
            if added:
                added_edges.append(edge)
                print(f"Step {frame + 1}: Added edge {edge}")
            else:
                print(f"Step {frame + 1}: Skipped edge {edge} (cycle)")

    ani = FuncAnimation(fig, update, frames=len(steps), interval=1000, repeat=False)  # 1 second delay for "real-time"
    plt.show()

# Main execution
if __name__ == "__main__":
    NUM_NODES = 8  # Customize as needed
    EDGE_PROB = 0.4  # Probability of edge between nodes

    graph = generate_random_graph(NUM_NODES, EDGE_PROB)
    if not nx.is_connected(graph):
        print("Generated graph is not connected. Regenerating...")
        graph = generate_random_graph(NUM_NODES, EDGE_PROB)  # Simple retry; in prod, ensure connectivity

    mst, steps = kruskal_mst(graph)
    total_weight = sum(data['weight'] for _, _, data in mst)
    print(f"MST Total Weight: {total_weight}")

    visualize_mst_animation(graph, steps)