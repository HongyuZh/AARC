host_cpu = 8
host_memory = 2048

if __name__ == "__main__":
    instances = [[0.25, 128], [0.5, 128], [0.75, 256]]
    host = [host_cpu, host_memory]
    num_hosts = 1
    assigned = []
    while len(instances) != 0:
        print("=" * 100)
        criteria = [
            abs((host[0] - instance[0]) / (host[1] - instance[1]) - host[0] / host[1])
            if host[0] >= instance[0] and host[1] >= instance[1]
            else 9999
            for instance in instances
        ]
        print(f"criteria: {criteria}")
        target = criteria.index(min(criteria))

        # assign instance to host
        if host[0] < instances[target][0] or host[1] < instances[target][1]:
            num_hosts += 1
            host = [host_cpu, host_memory]
        host[0] -= instances[target][0]
        host[1] -= instances[target][1]
        if host[0] <= 0 or host[1] <= 0:
            num_hosts += 1
            host = [host_cpu + min(0, host[0]), host_memory + min(0, host[1])]
        instances.pop(target)
        assigned.append({"instance": target, "host": num_hosts})
        print(f"instances: {instances}")
        print(f"num of hosts: {num_hosts}")
        print(f"host: {host}")
    print(f"assigned: {assigned}")
