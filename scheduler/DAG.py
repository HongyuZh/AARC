import matplotlib.pyplot as plt
import networkx as nx
from itertools import groupby


def generate_graph(runtime: list, dependencies: list):
    print(f"[+] Parsing the dependency graph...")
    DAG = nx.DiGraph()
    DAG.add_nodes_from(range(len(runtime)))
    for i, node in enumerate(DAG.nodes):
        DAG.nodes[node]["weight"] = runtime[i]
    DAG.add_edges_from(dependencies)
    return DAG


def critical_path(DAG: nx.DiGraph):
    print(f"[+] Finding critical path...")
    topo_order = list(nx.topological_sort(DAG))
    for node in DAG.nodes:
        DAG.nodes[node]["VE"] = 0

    # Forward pass
    for node in topo_order:
        for pred in DAG.predecessors(node):
            DAG.nodes[node]["VE"] = max(
                DAG.nodes[node]["VE"],
                DAG.nodes[pred]["VE"] + DAG.nodes[pred]["weight"],
            )

    for node in DAG.nodes:
        DAG.nodes[node]["VL"] = DAG.nodes[topo_order[-1]]["VE"]

    # Backward pass
    for node in reversed(topo_order):
        if not list(DAG.successors(node)):
            DAG.nodes[node]["VL"] = DAG.nodes[node]["VE"]
        else:
            for succ in DAG.successors(node):
                DAG.nodes[node]["VL"] = min(
                    DAG.nodes[node]["VL"],
                    DAG.nodes[succ]["VL"] - DAG.nodes[node]["weight"],
                )

    # Find critical path
    critical_node = []
    for node in DAG.nodes:
        if DAG.nodes[node]["VE"] == DAG.nodes[node]["VL"]:
            critical_node.append(node)

    print(f"[+] Critical path is found: {critical_node}")

    return critical_node


def DAG_draw(fig_name: str, DAG: nx.DiGraph, critical_node: list):
    critical_path = [
        (critical_node[i], critical_node[i + 1]) for i in range(len(critical_node) - 1)
    ]
    plt.figure(figsize=(5, 5))
    labels = nx.get_node_attributes(DAG, "weight")
    pos = nx.spring_layout(DAG)
    label_pos = {k: (v[0] + 0.1, v[1]) for k, v in pos.items()}
    edge_colors = ["red" if edge in critical_path else "orange" for edge in DAG.edges()]
    node_colors = ["red" if node in critical_node else "orange" for node in DAG.nodes()]
    nx.draw_networkx(
        DAG,
        pos=pos,
        with_labels=True,
        edge_color=edge_colors,
        node_color=node_colors,
    )
    nx.draw_networkx_labels(DAG, pos=label_pos, labels=labels, font_color="purple")
    plt.savefig(f"scheduler/image/DAG/{fig_name}.pdf")


def find_detour(DAG: nx.DiGraph, critical_node: list):
    print(f"[+] Finding detour paths...")

    # Find detour paths
    def find_path(start_node: int, end_node: int, valid_paths: list):
        if start_node == end_node:
            return
        else:
            simple_paths = nx.all_simple_paths(
                DAG, critical_node[start_node], critical_node[end_node]
            )
            for path in simple_paths:
                if any(node in critical_node for node in path[1:-1]) or len(path) <= 2:
                    continue
                valid_paths.append(path)
            find_path(start_node + 1, end_node, valid_paths)
            find_path(start_node, end_node - 1, valid_paths)

    detour = []
    find_path(0, len(critical_node) - 1, detour)
    detour = remove_duplicates(detour)
    sorted_detour = sort_by_edges(detour)
    print(f"[+] Detour paths are found: {sorted_detour}")

    print(f"[+] Creating subgraphs...")
    # Create subgraphs
    subgraphs = []
    for i, detours in enumerate(sorted_detour):
        subgraph = DAG.subgraph(list_union(detours))
        subgraphs.append(
            {
                "start_node": detours[0][0],
                "end_node": detours[0][-1],
                "subgraph": subgraph,
            }
        )

    return subgraphs


def remove_duplicates(array: list):
    unique_array = []
    seen = set()

    for sub_array in array:
        sub_tuple = tuple(sub_array)
        if sub_tuple not in seen:
            unique_array.append(sub_array)
            seen.add(sub_tuple)

    return unique_array


def sort_by_edges(arr: list):
    def get_first_element(item):
        return item[0]

    def get_last_element(item):
        return item[-1]

    sort_by_start = [list(group) for key, group in groupby(arr, key=get_first_element)]
    sort_by_end = []
    for sub_array in sort_by_start:
        sort_by_end += [
            list(group) for key, group in groupby(sub_array, key=get_last_element)
        ]
    return sort_by_end


def list_union(array: list):
    union_set = set()
    for sub_array in array:
        union_set = union_set.union(set(sub_array))
    return list(union_set)
