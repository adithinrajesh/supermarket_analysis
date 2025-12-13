from flask import Flask, render_template, request
from market_basket.market_basket_graph import (
    load_transactions,
    build_graph,
    bfs_related_items,
    find_matching_items,
    top_product_bundles
)

app = Flask(__name__)

@app.template_filter('replace_last')
def replace_last(value, old, new):
    """
    Replace last occurrence of old with new in a string
    """
    li = value.rsplit(old, 1)
    return new.join(li)


# Load data ONCE
transactions = load_transactions("data/supermarket_dataset.csv")
adjacency_list = build_graph(transactions)


@app.route("/", methods=["GET", "POST"])
def index():
    query_item = None
    suggestions = []
    results = []
    mode = "individual"
    limit = 5
    bundle_size = 2

    if request.method == "POST":
        user_input = request.form.get("item", "").strip()
        mode = request.form.get("mode", "individual")
        limit = int(request.form.get("limit", 5))
        bundle_size = int(request.form.get("bundle_size", 2))
        chosen_item = request.form.get("chosen_item")

        # User selected a suggestion
        if chosen_item:
            query_item = chosen_item
            if mode == "bundled":
                results = top_product_bundles(transactions, bundle_size=bundle_size, top_n=limit)
            else:
                related_items = bfs_related_items(query_item, adjacency_list, max_depth=2)
                results = list(related_items)[:limit]

        # User typed new input
        elif user_input:
            matches = find_matching_items(user_input, adjacency_list)
            if len(matches) == 1:
                query_item = matches[0]
                if mode == "bundled":
                    results = top_product_bundles(transactions, bundle_size=bundle_size, top_n=limit)
                else:
                    related_items = bfs_related_items(query_item, adjacency_list, max_depth=2)
                    results = list(related_items)[:limit]
            elif len(matches) > 1:
                suggestions = matches

    return render_template(
        "index.html",
        query_item=query_item,
        suggestions=suggestions,
        results=results,
        mode=mode,
        limit=limit,
        bundle_size=bundle_size
    )


if __name__ == "__main__":
    app.run(debug=True)
