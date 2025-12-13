from collections import defaultdict, deque
from itertools import combinations
import pandas as pd

def load_transactions(csv_path):
    """
    Load transactions from CSV and return a list of lists.
    Each inner list is the items bought by one customer in one visit.
    """
    df = pd.read_csv(csv_path)
    transactions = df.groupby(['Member_number', 'Date'])['itemDescription'].apply(list)
    return transactions.tolist()


def build_graph(transactions):
    """
    Build co-purchase graph using adjacency list.
    Each transaction is a list of items.
    """
    adjacency_list = defaultdict(lambda: defaultdict(int))

    for transaction in transactions:
        for i in range(len(transaction)):
            for j in range(i + 1, len(transaction)):
                item1, item2 = transaction[i], transaction[j]
                adjacency_list[item1][item2] += 1
                adjacency_list[item2][item1] += 1

    return adjacency_list


def bfs_related_items(start_item, adjacency_list, max_depth=2):
    """
    BFS to find related items up to max_depth away.
    """
    visited = set([start_item])
    queue = deque([(start_item, 0)])
    related_items = set()

    while queue:
        current, depth = queue.popleft()
        if depth >= max_depth:
            continue
        for neighbour in adjacency_list[current]:
            if neighbour not in visited:
                visited.add(neighbour)
                related_items.add(neighbour)
                queue.append((neighbour, depth + 1))

    return related_items


def find_matching_items(user_input, adjacency_list):
    """
    Return list of items that contain the user_input substring (case-insensitive)
    """
    user_input = user_input.lower()
    return [item for item in adjacency_list if user_input in item.lower()]


def top_product_bundles(transactions, bundle_size=2, top_n=6):
    """
    Compute top bundles of given size from transactions.
    Returns list of tuples: (bundle_tuple, frequency)
    """
    bundle_counts = defaultdict(int)
    for transaction in transactions:
        for combo in combinations(sorted(set(transaction)), bundle_size):
            bundle_counts[combo] += 1

    sorted_bundles = sorted(bundle_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_bundles[:top_n]

def items_frequently_bought_with_all(query_items, adjacency_list, top_n=6):
    """
    Return items most frequently bought with all query_items
    """
    if not query_items:
        return []

    # Start with first item's neighbors
    common_counts = adjacency_list.get(query_items[0], {}).copy()

    # Intersect with all other query_items
    for item in query_items[1:]:
        neighbors = adjacency_list.get(item, {})
        common_counts = {k: min(common_counts.get(k, 0), neighbors.get(k, 0))
                         for k in common_counts if k in neighbors}

    # Remove query_items themselves
    for q in query_items:
        common_counts.pop(q, None)

    # Sort top N
    sorted_items = sorted(common_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_items[:top_n]

import networkx as nx
import matplotlib.pyplot as plt

def visualize_item_network(adjacency_list, max_items=20, filename='graph.png'):
    """
    Visualize item co-purchase network
    max_items: limit nodes to top N items by degree for clarity
    """
    # Build graph
    G = nx.Graph()
    for item, neighbors in adjacency_list.items():
        for neighbor, weight in neighbors.items():
            if item < neighbor:  # avoid duplicate edges
                G.add_edge(item, neighbor, weight=weight)

    # Limit nodes if too many
    if len(G.nodes) > max_items:
        # Take top nodes by degree
        degrees = dict(G.degree(weight='weight'))
        top_nodes = sorted(degrees, key=degrees.get, reverse=True)[:max_items]
        G = G.subgraph(top_nodes).copy()

    # Draw
    pos = nx.spring_layout(G, seed=42)
    weights = [G[u][v]['weight'] for u,v in G.edges()]
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1000,
            edge_color='orange', width=[w/2 for w in weights], font_size=10)
    plt.title('Item Co-Purchase Network')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    return filename

def check_copurchase(item1, item2, adjacency_list, threshold=5):
    """
    Return True if item1 and item2 are co-purchased >= threshold
    """
    return adjacency_list[item1].get(item2, 0) >= threshold
