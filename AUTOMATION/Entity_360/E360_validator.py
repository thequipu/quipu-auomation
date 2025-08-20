# import json
# from collections import defaultdict, deque

# def validate_schema(schema_path):
#     with open(schema_path, "r") as f:
#         schema = json.load(f)

#     nodes = {n["id"]: n for n in schema.get("nodes", [])}
#     links = schema.get("links", [])

#     path_to_edges = defaultdict(list)
#     path_to_nodes = defaultdict(set)

#     # Collect nodes' pathIds
#     for node in schema.get("nodes", []):
#         for pid in node.get("pathIds", []):
#             path_to_nodes[pid].add(node["id"])

#     # Collect links' pathIds
#     for link in links:
#         for pid in link.get("pathIds", []):
#             path_to_edges[pid].append((link["source"], link["target"], link["relationship"]))
#             path_to_nodes[pid].add(link["source"])
#             path_to_nodes[pid].add(link["target"])

#     all_path_ids = set(path_to_nodes.keys()) | set(path_to_edges.keys())
#     report = {}

#     for pid in all_path_ids:
#         edges = path_to_edges.get(pid, [])
#         visited = set()
#         graph = defaultdict(list)

#         # Build adjacency list
#         for src, tgt, rel in edges:
#             graph[src].append(tgt)
#             graph[tgt].append(src)

#         # BFS for connectivity
#         if graph:
#             start = next(iter(graph))
#             q = deque([start])
#             while q:
#                 node = q.popleft()
#                 if node in visited:
#                     continue
#                 visited.add(node)
#                 q.extend(graph[node])

#         missing_nodes = [n for n in path_to_nodes[pid] if n not in nodes and n not in graph]

#         report[pid] = {
#             "total_nodes": len(path_to_nodes[pid]),
#             "total_edges": len(edges),
#             "connected": len(visited) == len(path_to_nodes[pid]) if edges else False,
#             "dangling": len(edges) == 0,
#             "missing_nodes": missing_nodes,
#         }

#     return report

#---------------------------------------------------------------------------------------------

import json
from collections import defaultdict, deque

def validate_schema(schema_path):
    with open(schema_path, "r") as f:
        schema = json.load(f)

    nodes = {n["id"]: n for n in schema.get("nodes", [])}
    links = schema.get("links", [])

    path_to_edges = defaultdict(list)
    path_to_nodes = defaultdict(set)

    # Collect nodes' pathIds
    for node in schema.get("nodes", []):
        for pid in node.get("pathIds", []):
            path_to_nodes[pid].add(node["id"])

    # Collect links' pathIds
    for link in links:
        for pid in link.get("pathIds", []):
            path_to_edges[pid].append((link["source"], link["target"], link["relationship"]))
            path_to_nodes[pid].add(link["source"])
            path_to_nodes[pid].add(link["target"])

    all_path_ids = set(path_to_nodes.keys()) | set(path_to_edges.keys())
    report = {}

    for pid in all_path_ids:
        edges = path_to_edges.get(pid, [])
        visited = set()
        graph = defaultdict(list)

        # Build adjacency list (undirected check)
        for src, tgt, rel in edges:
            graph[src].append(tgt)
            graph[tgt].append(src)

        # BFS for connectivity
        disconnected_nodes = []
        if graph:
            start = next(iter(graph))   # pick a start point
            q = deque([start])
            while q:
                node = q.popleft()
                if node in visited:
                    continue
                visited.add(node)
                q.extend(graph[node])

            # any pathId node not visited = unreachable
            disconnected_nodes = [n for n in path_to_nodes[pid] if n not in visited]

        missing_nodes = [n for n in path_to_nodes[pid] if n not in nodes and n not in graph]

        # Identify dangling details
        dangling_info = None
        if len(edges) == 0:
            # All nodes for this pathId are dangling start points
            dangling_info = list(path_to_nodes[pid])

        report[pid] = {
            "total_nodes": len(path_to_nodes[pid]),
            "total_edges": len(edges),
            "connected": len(visited) == len(path_to_nodes[pid]) if edges else False,
            "dangling": len(edges) == 0,
            "missing_nodes": missing_nodes,
            "dangling_nodes": dangling_info,       # isolated nodes when no edges
            "disconnected_nodes": disconnected_nodes  # 🔑 nodes that exist but aren’t reachable
        }

    return report
