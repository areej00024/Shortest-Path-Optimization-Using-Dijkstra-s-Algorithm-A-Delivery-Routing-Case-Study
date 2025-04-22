
#Flask App Setup
from flask import Flask, render_template, request, jsonify
import heapq

app = Flask(__name__)

#Main Page Rout
@app.route('/')
def index():
    return render_template("index.html")

#Run Dijkstra Route
@app.route('/run_dijkstra', methods=['POST'])

def run_dijkstra():
    #The graph is sent as JSON from the browser, and stored in the data variable
    data = request.json  
    #Extract Graph and Inputs
    edges = data.get("edges", [])
    source = data.get("source", "").strip().lower()
    destinations = [d.strip().lower() for d in data.get("destinations", [])]

    # Build graph as an adjacency list - Dictionary
    graph = {}
    for edge in edges:
        u = edge['from'].strip().lower()
        v = edge['to'].strip().lower()
        w = edge['cost']

        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []

        graph[u].append((v, w))
        graph[v].append((u, w))  # undirected graph

    #Check for Missing Source
    if source not in graph:
        return jsonify({"error": "Source node not found in the graph."})

    # Initialize Dijkstra
    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}
    dist[source] = 0
    queue = [(0, source)]

    #Run Dijkstra’s Main Loop
    while queue:
        current_dist, u = heapq.heappop(queue)
        for v, weight in graph.get(u, []):  # Edge Relaxation
            alt = current_dist + weight
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heapq.heappush(queue, (alt, v))

    # Path reconstruction
    def get_path(prev, source, dest):
        path = []
        while dest:
            path.insert(0, dest)
            dest = prev[dest]
        return path if path and path[0] == source else []

    #Build Results Dictionary
    results = {}
    for dest in destinations:
        if dest in graph:
            results[dest] = {
                "distance": dist[dest],
                "path": get_path(prev, source, dest)
            }
        else:
            results[dest] = {
                "distance": None,
                "path": [],
                "error": "Destination not found"
            }

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
