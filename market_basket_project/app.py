from flask import Flask, render_template, request
from market_basket.market_basket_graph import (
    load_transactions,
    build_graph,
    most_common_with,
    top_product_bundles,
    visualize_item_network_subgraph,
    format_individual_results,
    format_bundled_results
)

app = Flask(__name__)

# Load data and build adjacency list once at startup
transactions = load_transactions('data/supermarket_dataset.csv')
adjacency_list = build_graph(transactions)

@app.route('/', methods=['GET', 'POST'])
def index():
    mode = request.form.get('mode')
    query_item = request.form.get('item', '').strip()
    limit = int(request.form.get('limit', 6))
    bundle_size = int(request.form.get('bundle_size', 2))
    results = []
    graph_file = None

    if mode == 'individual' and query_item:
        top_items = most_common_with(query_item, adjacency_list, top_n=limit)
        results = format_individual_results(top_items)
        # Nodes for graph include main item + related items
        nodes = [query_item] + [item for item, _ in top_items]
        graph_file = visualize_item_network_subgraph(adjacency_list, nodes)

    elif mode == 'bundled' and transactions:
        top_bundles = top_product_bundles(transactions, top_n=limit, bundle_size=bundle_size)
        results = format_bundled_results(top_bundles)
        # Nodes for graph include all items in top bundles
        nodes = set()
        for bundle, _ in top_bundles:
            nodes.update(bundle)
        if nodes:
            graph_file = visualize_item_network_subgraph(adjacency_list, list(nodes))

    return render_template(
        'index.html',
        mode=mode,
        query_item=query_item,
        limit=limit,
        bundle_size=bundle_size,
        results=results,
        graph_file=graph_file
    )

if __name__ == '__main__':
    app.run(debug=True)
