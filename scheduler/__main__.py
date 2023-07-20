import pickle

import matplotlib.pyplot as plt
import networkx as nx
from colorama import Fore
from utils.container import Container

from .DAG import DAG_draw, critical_path, find_detour, generate_graph
from .priority_schedule import priority_schedule


def schedule(SLO: int, DAG: nx.DiGraph):
    global containers
    global init_DAG
    global counter

    critical_node = critical_path(DAG)
    to_be_scheduled = []
    to_be_scheduled_index = []
    for node in critical_node:
        if not DAG.nodes[node]["scheduled"]:
            to_be_scheduled.append(containers[node])
            to_be_scheduled_index.append(node)
        else:
            print(
                f"{Fore.CYAN}[+] Container_{node} is already scheduled, subtract its runtime: {containers[node].runtime}{Fore.RESET}"
            )
            SLO -= containers[node].runtime
    print(
        f"{Fore.CYAN}[+] Containers to be scheduled: {to_be_scheduled_index}{Fore.RESET}"
    )
    print(f"{Fore.CYAN}[+] SLO is: {SLO}{Fore.RESET}")
    priority_schedule(to_be_scheduled, SLO)
    for node in to_be_scheduled_index:
        DAG.nodes[node]["scheduled"] = True
        DAG.nodes[node]["weight"] = containers[node].runtime
        init_DAG.nodes[node]["scheduled"] = True
        init_DAG.nodes[node]["weight"] = containers[node].runtime
    pos = {
        0: (0, 3),
        1: (1, 2),
        2: (1, 5),
        3: (2, 4),
        4: (2, 6),
        5: (3, 5),
        6: (5, 4),
        7: (3, 1),
        8: (3, 3),
        9: (6, 3),
    }
    DAG_draw(f"DAG_{counter}", init_DAG, critical_node, pos)
    counter += 1

    subgraphs = find_detour(DAG, critical_node)
    if subgraphs:
        for item in subgraphs:
            start_node = item["start_node"]
            end_node = item["end_node"]
            subgraph = item["subgraph"]
            start_index = critical_node.index(start_node)
            end_index = critical_node.index(end_node)
            new_SLO = sum(
                [
                    containers[i].runtime
                    for i in critical_node[start_index : end_index + 1]
                ]
            )
            print(f"{Fore.CYAN}[+] Generating new SLO: {new_SLO}{Fore.RESET}")
            schedule(new_SLO, subgraph)
    else:
        return


if __name__ == "__main__":
    images = [
        "matmul:v1",
        "float_operation:v1",
        "pyaes:v1",
        "matmul:v1",
        "float_operation:v1",
        "pyaes:v1",
        "matmul:v1",
        "float_operation:v1",
        "pyaes:v1",
        "matmul:v1",
    ]
    runtime = []
    containers = []
    for image in images:
        container = Container(image, memory=544, cpu=2.25)
        container.run()
        runtime.append(container.runtime)
        containers.append(container)
    dependencies = [
        (0, 1),
        (0, 2),
        (1, 7),
        (1, 8),
        (2, 3),
        (2, 4),
        (3, 5),
        (4, 5),
        (5, 6),
        (6, 9),
        (7, 9),
        (8, 9),
    ]
    init_DAG = generate_graph(runtime, dependencies)
    counter = 0
    for node in init_DAG.nodes:
        init_DAG.nodes[node]["scheduled"] = False
    schedule(3000, init_DAG)

    for i, container in enumerate(containers):
        with open(f"scheduler/data/func/fun_{i}.pkl", "wb") as f:
            pickle.dump(container.recorder, f)
        container.delete()
