from flask import Flask, render_template, request
from market_basket.market_basket_graph import (
    load_transactions,
    build_graph,
    most_common_with
)

app = Flask(__name__)

# Load data ONCE when app starts
transactions = load_transactions("data/supermarket_dataset.csv")
graph = build_graph(transactions)

@app.route("/", methods=["GET", "POST"])
def index():
    items = []

    if request.method == "POST":
        item = request.form.get("item")
        if item:
            items = most_common_with(item, graph)

    return render_template("index.html", items=items)

if __name__ == "__main__":
    app.run(debug=True)
