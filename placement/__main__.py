import pickle

host_cpu = 8
host_memory = 2048


def first_fit():
    global instances
    global hosts
    global num_hosts

    assigned = []
    while len(instance) > 0:
        print("=" * 100)
        for instance in instances:
            for host in hosts:
                if host[0] > instance["config"][0] and host[1] > instance["config"][1]:
                    # assign instance to host
                    host[0] -= instance["config"][0]
                    host[1] -= instance["config"][1]
                    assigned.append(
                        {
                            "instance": instance["index"],
                            "host": num_hosts,
                        }
                    )
                    instances.pop(instance)
            else:
                num_hosts += 1
                hosts.append([host_cpu, host_memory])


def best_fit():
    global instances
    global hosts
    global num_hosts

    assigned = []
    while len(instances) > 0:
        print("=" * 100)
        criteria = []
        for instance in instances:
            for host in hosts:
                if host[0] > instance["config"][0] and host[1] > instance["config"][1]:
                    criteria.append(
                        abs(
                            (host[0] - instance["config"][0])
                            / (host[1] - instance["config"][1])
                            - host[0] / host[1]
                        )
                    )
                elif (
                    host[0] == instance["config"][0] and host[1] > instance["config"][1]
                ):
                    criteria.append(-instance["config"][1] / host[1])
                elif (
                    host[0] > instance["config"][0] and host[1] == instance["config"][1]
                ):
                    criteria.append(-instance["config"][0] / host[0])
                else:
                    criteria.append(float("inf"))
            if min(criteria) == float("inf"):
                num_hosts += 1
                hosts.append([host_cpu, host_memory])
                continue
            target = criteria.index(min(criteria))

        # assign instance to host
        hosts[target][0] -= instances[target]["config"][0]
        hosts[target][1] -= instances[target]["config"][1]
        assigned.append(
            {
                "instance": instances[target]["index"],
                "host": num_hosts,
            }
        )
        instances.pop(target)


if __name__ == "__main__":
    instances = []
    for i in range(33):
        instances.append({"index": 3 * i, "config": [1, 128]})
        instances.append({"index": 3 * i + 1, "config": [2, 256]})
        instances.append({"index": 3 * i + 2, "config": [4, 512]})

    hosts = [[host_cpu, host_memory]]
    num_hosts = 1
    assigned = []
    while len(instances) != 0:
        print("=" * 100)
        criteria = []
        for instance in instances:
            if (
                hosts[-1][0] > instance["config"][0]
                and hosts[-1][1] > instance["config"][1]
            ):
                criteria.append(
                    abs(
                        (hosts[-1][0] - instance["config"][0])
                        / (hosts[-1][1] - instance["config"][1])
                        - hosts[-1][0] / hosts[-1][1]
                    )
                )
            elif (
                hosts[-1][0] == instance["config"][0]
                and hosts[-1][1] > instance["config"][1]
            ):
                criteria.append(-instance["config"][1] / hosts[-1][1])
            elif (
                hosts[-1][0] > instance["config"][0]
                and hosts[-1][1] == instance["config"][1]
            ):
                criteria.append(-instance["config"][0] / hosts[-1][0])
            else:
                criteria.append(float("inf"))
        if min(criteria) == float("inf"):
            num_hosts += 1
            hosts.append([host_cpu, host_memory])
            continue
        target = criteria.index(min(criteria))

        # assign instance to host
        hosts[-1][0] -= instances[target]["config"][0]
        hosts[-1][1] -= instances[target]["config"][1]
        assigned.append(
            {
                "instance": instances[target]["index"],
                "host": num_hosts,
            }
        )
        instances.pop(target)
        print(f"num of hosts: {num_hosts}")
        print(f"host: {hosts[-1]}")
    print(f"assigned: {assigned}")

    recorder = {"CPU": 0, "memory": 0}
    for host in hosts:
        recorder["CPU"] += host[0]
        recorder["memory"] += host[1]

    with open(f"placement/data/recorder.pkl", "wb") as f:
        pickle.dump(recorder, f)
