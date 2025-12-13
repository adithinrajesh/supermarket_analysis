from collections import defaultdict

def build_graph(transactions):
    """
    Build a co-purchase graph from a list of transactions.
    Each transaction is a list of items.
    
    Returns:
        graph (dict): {item1: {item2: frequency, ...}, ...}
    """
    # Initialize an empty graph
    graph = defaultdict(lambda: defaultdict(int))

    # Loop through each transaction
    for transaction in transactions:
        # Loop through all pairs of items in the transaction
        for i in range(len(transaction)):
            for j in range(i + 1, len(transaction)):
                item1, item2 = transaction[i], transaction[j]
                
                # Increment edge weight for both directions
                graph[item1][item2] += 1
                graph[item2][item1] += 1

    return graph

def most_common_with(item, graph, top_n=6):
    """Return the top N items most frequently bought with the given item."""
    if item not in graph:
        return []
    sorted_items = sorted(graph[item].items(), key=lambda x: x[1], reverse=True)
    return sorted_items[:top_n]

def are_often_copurchased(item1, item2, graph, threshold=6):
    """Check if two items are frequently co-purchased."""
    return graph[item1].get(item2, 0) >= threshold

def top_product_bundles(graph, top_n=6):
    """Return the top N item pairs with highest co-purchase frequency."""
    seen = set()
    bundles = []
    for item1, edges in graph.items():
        for item2, count in edges.items():
            if (item2, item1) not in seen:
                bundles.append(((item1, item2), count))
                seen.add((item1, item2))
    return sorted(bundles, key=lambda x: x[1], reverse=True)[:top_n]

import pandas as pd

def load_transactions(csv_path):
    """
    Load transactions from CSV and return a list of lists.
    Each inner list is the items bought by one customer in one visit.
    """
    df = pd.read_csv(csv_path)
    # Group by Member_number and Date to get transactions
    transactions = df.groupby(['Member_number', 'Date'])['itemDescription'].apply(list)
    return transactions.tolist()

# Example usage
csv_path = 'data/supermarket_dataset.csv'
transactions = load_transactions(csv_path)
graph = build_graph(transactions) 