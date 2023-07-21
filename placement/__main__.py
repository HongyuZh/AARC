host_cpu = 8
host_memory = 2048

if __name__ == "__main__":
    instances = []
    for i in range(33):
        instances.append({"index": 3 * i, "config": [1, 128]})
        instances.append({"index": 3 * i + 1, "config": [2, 256]})
        instances.append({"index": 3 * i + 2, "config": [4, 512]})

    host = [host_cpu, host_memory]
    num_hosts = 1
    assigned = []
    while len(instances) != 0:
        print("=" * 100)
        criteria = []
        for instance in instances:
            if host[0] > instance["config"][0] and host[1] > instance["config"][1]:
                criteria.append(
                    abs(
                        (host[0] - instance["config"][0])
                        / (host[1] - instance["config"][1])
                        - host[0] / host[1]
                    )
                )
            elif host[0] == instance["config"][0] and host[1] > instance["config"][1]:
                criteria.append(-instance["config"][1] / host[1])
            elif host[0] > instance["config"][0] and host[1] == instance["config"][1]:
                criteria.append(-instance["config"][0] / host[0])
            else:
                criteria.append(float("inf"))
        if min(criteria) == float("inf"):
            num_hosts += 1
            host = [host_cpu, host_memory]
            continue
        target = criteria.index(min(criteria))

        # assign instance to host
        host[0] -= instances[target]["config"][0]
        host[1] -= instances[target]["config"][1]
        assigned.append(
            {
                "instance": instances[target]["index"],
                "host": num_hosts,
            }
        )
        instances.pop(target)
        print(f"num of hosts: {num_hosts}")
        print(f"host: {host}")
    print(f"assigned: {assigned}")
