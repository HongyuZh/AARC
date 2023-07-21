from utils.priorityQueue import PriorityQueue
from utils.container import Container
from colorama import Fore


def push_op(container: Container, tag: str, pq: PriorityQueue):
    old_cost = container.cost
    op = {"tag": tag}
    if tag == "cpu":
        container.updateAllocation(cpu=container.cpu - 0.25)
        op["step"] = 0.5
    elif tag == "memory":
        container.updateAllocation(memory=container.memory - 32)
        op["step"] = 256
    container.run()
    op["fun"] = container
    op["trail"] = 3
    pq.push(op, old_cost - container.cost)


def priority_schedule(containers: list, SLO: int):
    pq = PriorityQueue()

    # initialization
    recorder = {"runtime": [0], "cost": [0], "SLO": SLO}
    for container in containers:
        push_op(container, "cpu", pq)
        push_op(container, "memory", pq)
        recorder["runtime"][0] += container.runtime
        recorder["cost"][0] += container.cost
    print(
        "[+] All functions are push into priority queue, "
        f"with runtime: {Fore.GREEN}{recorder['runtime'][0]} ms{Fore.RESET} and cost: {Fore.GREEN}{recorder['cost'][0]} ${Fore.RESET}"
    )

    # scheduling
    while pq.notEmpty():
        print("=" * 100)
        op = pq.pop()
        container = op["fun"]
        old_runtime = op["fun"].runtime
        old_cost = op["fun"].cost

        # deallocation
        print(
            f"{Fore.YELLOW}[+]{Fore.RESET} Deallocate {op['tag']} from container ({container.image_id}[{container.container_id}])"
        )
        if op["tag"] == "cpu":
            if container.cpu <= op["step"]:
                print(
                    f"{Fore.YELLOW}[+]{Fore.RESET} Reaching the minimum allocation, continue..."
                )
                continue
            container.updateAllocation(cpu=container.cpu - op["step"])
            if op["step"] > 0.25:
                op["step"] /= 2
        elif op["tag"] == "memory":
            if container.memory <= op["step"]:
                print(
                    f"{Fore.YELLOW}[+]{Fore.RESET} Reaching the minimum allocation, continue..."
                )
                continue
            container.updateAllocation(memory=container.memory - op["step"])
            if op["step"] > 32:
                op["step"] /= 2

        container.run()
        recorder["runtime"].append(
            recorder["runtime"][-1] + container.runtime - old_runtime
        )
        recorder["cost"].append(recorder["cost"][-1] + container.cost - old_cost)
        print(
            f"{Fore.YELLOW}[+]{Fore.RESET} Update runtime: {Fore.GREEN}{recorder['runtime'][-1]} ms{Fore.RESET} and cost: {Fore.GREEN}{recorder['cost'][-1]} ${Fore.RESET}"
        )

        # violation handler
        if recorder["runtime"][-1] > SLO or op["fun"].cost > old_cost * (1 + 0.05):
            print(f"{Fore.YELLOW}[+]{Fore.RESET} Violation detected, rollback...")
            if op["tag"] == "cpu":
                container.updateAllocation(cpu=container.cpu + 0.25)
            elif op["tag"] == "memory":
                container.updateAllocation(memory=container.memory + 32)
            container.runtime = old_runtime
            container.cost = old_cost
            recorder["runtime"].append(recorder["runtime"][-2])
            recorder["cost"].append(recorder["cost"][-2])
            print(
                f"{Fore.YELLOW}[+]{Fore.RESET} Update runtime: {Fore.GREEN}{recorder['runtime'][-1]} ms{Fore.RESET} and cost: {Fore.GREEN}{recorder['cost'][-1]} ${Fore.RESET}"
            )
            op["trail"] -= 1
            if op["trail"] > 0:
                pq.push(op, 0)
                continue
            print(
                f"{Fore.YELLOW}[+]{Fore.RESET} Container ({container.image_id}[{container.container_id}]) is removed from priority queue"
            )
        else:
            print(f"{Fore.YELLOW}[+]{Fore.RESET} Successfull allocation")
            op["trail"] = 3
            pq.push(op, min(old_cost - container.cost, 0))
    print(f"{Fore.YELLOW}[+]{Fore.RESET} Done")

    return recorder
