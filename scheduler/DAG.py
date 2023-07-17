import matplotlib.pyplot as plt
import networkx as nx


def critical_path(runtime: list, dependencies: list, draw: bool = False):
    """
    Given the dependencies and runtime of each function,
    draw a graph of the workflow and return the critical path.

    ## Parameters
    - runtime: A list of runtime of each function.
    - dependencies: A list of dependencies of each function, represented by [(predecessor, successor)].

    ## Returns
    - critical_node: A list of critical nodes in the workflow.
    - detour: A list of detour paths in the workflow.
    """
    print(f"[+] Parsing the dependency graph...")
    DAG = nx.DiGraph()
    DAG.add_nodes_from(range(len(runtime)))
    for i, node in enumerate(DAG.nodes):
        DAG.nodes[node]["weight"] = runtime[i]
    DAG.add_edges_from(dependencies)

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
    critical_path = [
        (critical_node[i], critical_node[i + 1]) for i in range(len(critical_node) - 1)
    ]
    print(f"[+] Critical path is found: {critical_node}")

    # Draw the DAG
    if draw:
        plt.figure(figsize=(5, 5))
        labels = nx.get_node_attributes(DAG, "weight")
        pos = nx.spring_layout(DAG)
        label_pos = {k: (v[0] + 0.1, v[1]) for k, v in pos.items()}
        edge_colors = [
            "red" if edge in critical_path else "orange" for edge in DAG.edges()
        ]
        node_colors = [
            "red" if node in critical_node else "orange" for node in DAG.nodes()
        ]
        nx.draw_networkx(
            DAG,
            pos=pos,
            with_labels=True,
            edge_color=edge_colors,
            node_color=node_colors,
        )
        nx.draw_networkx_labels(DAG, pos=label_pos, labels=labels, font_color="purple")
        plt.savefig("scheduler/image/DAG.pdf")
        print(f"[+] DAG is drawn: scheduler/image/DAG.pdf")

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
    print(f"[+] Detour paths are found: {detour}")

    return critical_node, detour


def remove_duplicates(arr):
    unique_arr = []
    seen = set()

    for sublist in arr:
        sub_tuple = tuple(sublist)

        if sub_tuple not in seen:
            unique_arr.append(sublist)
            seen.add(sub_tuple)

    return unique_arr
