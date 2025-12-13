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
