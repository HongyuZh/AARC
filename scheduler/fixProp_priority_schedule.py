from utils.priorityQueue import PriorityQueue
from utils.container import Container
from colorama import Fore


def push_op(container: Container, pq: PriorityQueue):
    old_cost = container.cost
    op = {}
    container.updateAllocation(cpu=container.cpu - 0.25, memory=container.memory - 32)
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
        push_op(container, pq)
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
        step = op["step"]
        old_runtime = op["fun"].runtime
        old_cost = op["fun"].cost

        # deallocation
        print(
            f"{Fore.YELLOW}[+]{Fore.RESET} Deallocate container ({container.image_id}[{container.container_id}])"
        )
        if container.memory <= step or container.cpu <= step / 128:
            print(
                f"{Fore.YELLOW}[+]{Fore.RESET} Reaching the minimum allocation, continue..."
            )
            continue
        container.updateAllocation(
            memory=container.memory - step, cpu=container.cpu - step / 128
        )
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
            container.updateAllocation(
                memory=container.memory + step, cpu=container.cpu + step / 128
            )
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
