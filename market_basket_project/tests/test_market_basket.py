import pytest
from market_basket.market_basket_graph import build_graph, most_common_with, are_often_copurchased, top_product_bundles

def test_build_graph_and_most_common_with():
    transactions = [
        ['bread', 'milk'],
        ['bread', 'eggs'],
        ['milk', 'bread'],
        ['eggs', 'bread', 'milk']
    ]
    graph = build_graph(transactions)
    
    # Test most_common_with
    result = most_common_with('bread', graph)
    assert result[0][0] == 'milk'  # milk should be the most co-purchased with bread
    assert result[0][1] == 3       # milk appears 3 times with bread

def test_are_often_copurchased():
    transactions = [['bread', 'milk']] * 6
    graph = build_graph(transactions)
    assert are_often_copurchased('bread', 'milk', graph, threshold=5) == True
    assert are_often_copurchased('bread', 'eggs', graph, threshold=1) == False

def test_top_product_bundles():
    transactions = [
        ['bread', 'milk'],
        ['bread', 'eggs'],
        ['milk', 'bread'],
        ['eggs', 'bread', 'milk']
    ]
    graph = build_graph(transactions)
    top_bundles = top_product_bundles(graph, top_n=2)
    assert top_bundles[0][0] == ('bread', 'milk') or top_bundles[0][0] == ('milk', 'bread')
