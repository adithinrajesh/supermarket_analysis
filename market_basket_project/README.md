# Supermarket Basket Recommendation System

A Python-based web application for analysing supermarket transaction data and 
providing product recommendations based on co-purchase patterns. The system models
item relationships using graph-based data structures and supports both individual item
recommendations and bundled product analysis.

---

## Features
- Graph-based representation of item co-purchases
- Individual item recommendations (e.g. “Items frequently bought with bread”)
- Bundled product recommendations (top N itemsets)
- Clean web interface built with Flask

---

## Data Structures and Algorithms

### Data Structure
- Weighted undirected graph implemented using adjacency lists
- Nodes represent items
- Edge weights represent co-purchase frequency

### Algorithms Implemented
- Co-occurrence graph construction
- Sorting and ranking of associated items
- Frequent itemset (bundle) enumeration
- Breadth-First Search (BFS) for related item exploration
- Graph filtering and subgraph extraction

---

## Visualisation

- Item association networks are visualised using NetworkX and Matplotlib
- Stronger associations are highlighted using edge weight filtering
- Graphs update dynamically based on user queries

---

## Getting Started

### Prerequisites
- Python 3.9 or later

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/supermarket-basket-recommender.git
   cd supermarket-basket-recommender
2. install dependencies
   pip install -r requirements.txt
3. run the application
   python app.py
4. open your browser and visit
   http://127.0.0.1:5000/

### Dataset

Format: CSV
Columns:
Member_number
Date
itemDescription

