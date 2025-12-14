from flask import Flask, render_template, request

# Import market basket analysis utilities
# These functions handle data loading, graph construction, recommendation logic, formatting, and visualisation
from market_basket.market_basket_graph import (
    load_transactions,
    build_graph,
    most_common_with,
    top_product_bundles,
    visualize_item_network_subgraph,
    format_individual_results,
    format_bundled_results
)

# Create Flask application instance
app = Flask(__name__)

# --------------------------------
# Data Loading and Preprocessing 
# --------------------------------
transactions = load_transactions('data/supermarket_dataset.csv')
adjacency_list = build_graph(transactions)

# --------------------------
# Main Application Route
# --------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Main route handling both page rendering and recommendation queries.
    Supports two modes:
    - Individual item recommendations
    - Bundled product recommendations
    """

    # Retrieve selected mode (individual or bundled)
    mode = request.form.get('mode')

    # Retrieve item entered by the user (if any)
    query_item = request.form.get('item', '').strip()

    # Number of results to display (used in both modes)
    limit = int(request.form.get('limit', 6))

    # Bundle size for bundled recommendations
    bundle_size = int(request.form.get('bundle_size', 2))

    # Containers for results and graph image path
    results = []
    graph_file = None

    # ---------------------------------
    # Individual Recommendation Mode
    # ---------------------------------
    if mode == 'individual' and query_item:
        # Find items most frequently bought with the selected item
        top_items = most_common_with(query_item, adjacency_list, top_n=limit)

        # Format results into user-friendly sentences
        results = format_individual_results(top_items)

        # Prepare nodes for visualisation:
        # main queried item + its top related items
        nodes = [query_item] + [item for item, _ in top_items]

        # Generate and save the co-purchase network graph
        graph_file = visualize_item_network_subgraph(adjacency_list, nodes)

    # -----------------------------
    # Bundled Recommendation Mode
    # -----------------------------
    elif mode == 'bundled' and transactions:
        # Identify top frequent product bundles of selected size
        top_bundles = top_product_bundles(
            transactions,
            top_n=limit,
            bundle_size=bundle_size
        )

        # Format bundle results for display
        results = format_bundled_results(top_bundles)

        # Collect all unique items from top bundles for graph visualisation
        nodes = set()
        for bundle, _ in top_bundles:
            nodes.update(bundle)

        # Generate network graph if there are items to display
        if nodes:
            graph_file = visualize_item_network_subgraph(
                adjacency_list,
                list(nodes)
            )

    # ----------------------
    # Render HTML Template
    # ----------------------
    return render_template(
        'index.html',
        mode=mode,
        query_item=query_item,
        limit=limit,
        bundle_size=bundle_size,
        results=results,
        graph_file=graph_file
    )

# --------------------------
# Application Entry Point
# --------------------------
if __name__ == '__main__':
    # Run Flask app in debug mode (development only)
    app.run(debug=True)