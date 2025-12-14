from collections import defaultdict, deque
import pandas as pd
import networkx as nx
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for Flask
import matplotlib.pyplot as plt
from itertools import combinations

# ---------------------------
# Data Loading
# ---------------------------
def load_transactions(csv_path):
    """
    Load supermarket dataset and group items by member and date.
    Returns a list of transactions (list of items).
    """
    df = pd.read_csv(csv_path)
    transactions = df.groupby(['Member_number', 'Date'])['itemDescription'].apply(list)
    return transactions.tolist()

# ---------------------------
# Graph Construction
# ---------------------------
def build_graph(transactions):
    """
    Build adjacency list for co-purchased items.
    adjacency_list[item1][item2] = number of times item1 and item2 were bought together
    """
    adjacency_list = defaultdict(lambda: defaultdict(int))
    for transaction in transactions:
        for i in range(len(transaction)):
            for j in range(i + 1, len(transaction)):
                item1, item2 = transaction[i], transaction[j]
                adjacency_list[item1][item2] += 1
                adjacency_list[item2][item1] += 1
    return adjacency_list

# ---------------------------
# Individual Recommendations
# ---------------------------
def most_common_with(item, adjacency_list, top_n=6):
    """
    Return top N items most frequently bought with the given item.
    """
    if item not in adjacency_list:
        return []
    return sorted(adjacency_list[item].items(), key=lambda x: x[1], reverse=True)[:top_n]

def bfs_related_items(start_item, adjacency_list, max_depth=2):
    """
    Optional: BFS traversal to get related items up to a certain depth.
    """
    visited = set([start_item])
    queue = deque([(start_item, 0)])
    related_items = set()
    while queue:
        current, depth = queue.popleft()
        if depth >= max_depth:
            continue
        for neighbor in adjacency_list[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                related_items.add(neighbor)
                queue.append((neighbor, depth + 1))
    return related_items

# ---------------------------
# Bundled Recommendations
# ---------------------------
def top_product_bundles(transactions, top_n=6, bundle_size=2):
    """
    Return the top N bundles of items frequently bought together.
    Each bundle is a tuple (items_tuple, count)
    """
    bundle_counts = defaultdict(int)
    for transaction in transactions:
        unique_items = sorted(set(transaction))
        if len(unique_items) >= bundle_size:
            for combo in combinations(unique_items, bundle_size):
                bundle_counts[combo] += 1
    sorted_bundles = sorted(bundle_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_bundles[:top_n]

# ---------------------------
# Graph Visualization
# ---------------------------
def visualize_item_network_subgraph(adjacency_list, nodes, filename='static/images/graph.png'):
    """
    Generate and save a circular network graph of co-purchased items.
    Includes self-loops styled as arcs, with all nodes light blue.
    """
    import networkx as nx
    import matplotlib.pyplot as plt

    # Build graph
    G = nx.Graph()
    for item in nodes:
        for neighbor, weight in adjacency_list[item].items():
            if neighbor in nodes and weight >= 2:
                G.add_edge(item, neighbor, weight=weight)

    if len(G.nodes) == 0:
        return None

    # Circular layout for symmetry
    pos = nx.circular_layout(G)

    # Node sizes by degree, all light blue
    node_sizes = [300 + 150 * G.degree(n) for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='lightblue')

    # Separate normal edges and self-loops
    normal_edges = [(u, v) for u, v in G.edges() if u != v]
    loop_edges = [(u, v) for u, v in G.edges() if u == v]

    # Edge widths scaled gently
    weights = [G[u][v]['weight'] for u, v in normal_edges]
    max_w = max(weights) if weights else 1
    edge_widths = [0.5 + (w / max_w) * 2.5 for w in weights]

    # Draw normal edges
    nx.draw_networkx_edges(G, pos, edgelist=normal_edges,
                           width=edge_widths, edge_color='gray', alpha=0.6)

    # Draw self-loops as arcs
    if loop_edges:
        nx.draw_networkx_edges(G, pos, edgelist=loop_edges,
                               connectionstyle="arc3,rad=0.3",
                               edge_color='gray', alpha=0.6, width=2)

    # Labels: show item name and self-loop count if present
    labels = {}
    for n in G.nodes():
        if (n, n) in G.edges():
            labels[n] = f"{n}\n({G[n][n]['weight']})"
        else:
            labels[n] = n

    nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_color='black')

    # Optional: edge labels for weights (excluding self-loops)
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True) if u != v}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title('Item Association Graph', fontsize=16)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    return filename
# ---------------------------
# Formatting Helpers
# ---------------------------
def format_individual_results(results):
    """
    Format individual recommendation results for display.
    """
    return [f"{item.capitalize()} — {count} times" for item, count in results]

def format_bundled_results(results):
    """
    Format bundled recommendation results for display.
    Handles 2+ item bundles with proper grammar.
    """
    formatted = []
    for bundle, count in results:
        if len(bundle) == 2:
            sentence = f"{bundle[0].capitalize()} and {bundle[1].capitalize()} were bought together {count} times."
        else:
            all_but_last = ", ".join([x.capitalize() for x in bundle[:-1]])
            sentence = f"{all_but_last} and {bundle[-1].capitalize()} were bought together {count} times."
        formatted.append(sentence)
    return formatted
