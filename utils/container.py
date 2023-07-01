import time

import docker
from colorama import Fore, Style
from prettytable import PrettyTable

client = docker.from_env()


def wait_complete():
    while True:
        activeContainers = client.containers.list()

        if len(activeContainers) == 0:
            break
        else:
            time.sleep(1)


class Container:
    def __init__(self, image_id, memory, cpu):
        self.image_id = image_id
        self.memory = memory
        self.cpu = cpu
        self.container_id = self._init_container()
        self.runtime = 0
        self.cost = 0
        self.recorder = []

        print(
            f"[+] Container ({self.image_id}[{self.container_id}]) is created with {Fore.GREEN}{self.memory} MB{Fore.RESET} memory and {Fore.GREEN}{self.cpu}{Fore.RESET} CPU(s)"
        )

    def _init_container(self):
        try:
            container = client.containers.create(
                self.image_id,
                detach=True,
                mem_limit=f"{self.memory}M",
                memswap_limit=f"{self.memory}M",
                cpu_period=100000,
                cpu_quota=int(self.cpu * 100000),
            )
        except docker.errors.ImageNotFound:
            print(f"{Fore.RED}[ERROR]{Fore.RESET} image not found ({self.image_id})")
            exit(1)

        return container.short_id

    def run(self, autodelete=False):
        print(f"[+] Container ({self.image_id}[{self.container_id}]) is running...")
        container = client.containers.get(self.container_id)
        wait_complete()
        container.restart()
        wait_complete()

        log = str(container.logs(), encoding="utf-8").strip()
        if log.split("\n")[-1] == "Killed":
            print(
                f"{Fore.YELLOW}[!]{Fore.RESET} container is killed, maybe {Fore.RED}{Style.BRIGHT}OOM{Style.RESET_ALL}{Fore.RESET} occurred"
            )
            if autodelete:
                self.delete()
            self.recorder.append([self.memory, self.cpu, "-", "-"])
            exit(1)
        self.runtime = int(log.split(":")[-1])
        self.cost = self.runtime * (self.memory + self.cpu * 512) / 1000
        self.recorder.append([self.memory, self.cpu, self.runtime, self.cost])

        print(
            f"[+] Running finished with runtime: {Fore.GREEN}{self.runtime} ms{Fore.RESET}"
            f" and cost: {Fore.GREEN}{self.cost}{Fore.RESET}"
        )

    def updateAllocation(self, memory=None, cpu=None):
        if memory is not None:
            self.memory = memory
        if cpu is not None:
            self.cpu = cpu
        container = client.containers.get(self.container_id)
        container.update(
            mem_limit=f"{self.memory}M",
            memswap_limit=f"{self.memory}M",
            cpu_period=100000,
            cpu_quota=int(self.cpu * 100000),
        )
        print(
            f"[+] Container ({self.image_id}[{self.container_id}]) is updated with {Fore.GREEN}{self.memory} MB{Fore.RESET} memory and {Fore.GREEN}{self.cpu}{Fore.RESET} CPU(s)"
        )

    def display(self, save=False):
        table = PrettyTable()
        table.field_names = ["Index", "Memory", "CPU", "Runtime", "Cost"]
        for i, record in enumerate(self.recorder):
            table.add_row([i, *record])
        print(f"[+] The profiling is displayed as follows:")
        print(table)

    def delete(self):
        try:
            container = client.containers.get(self.container_id)
        except AttributeError:
            print(f"[-] No container created, exit...")
            return
        container.remove()
        print(
            f"[+] Container ({self.image_id}[{self.container_id}]) is deleted: {self.container_id} ({self.image_id})"
        )
