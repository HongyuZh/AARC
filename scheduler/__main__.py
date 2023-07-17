from .DAG import critical_path
from .priority_schedule import priority_schedule
from utils.container import Container
import matplotlib.pyplot as plt

if __name__ == "__main__":
    runtime = [7, 2, 4, 6, 3, 5, 4, 2, 1, 5]
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
    critical_path(runtime, dependencies)

    images = ["matmul:v1", "float_operation:v1", "pyaes:v1"]
    containers = []
    for image in images:
        containers.append(Container(image, memory=544, cpu=2.25))
    runtime, cost = priority_schedule(containers, 1500)
    for container in containers:
        container.delete()

    plt.figure()
    plt.plot(runtime, label="runtime")
    plt.plot(cost, label="cost")
    plt.legend()
    plt.savefig("scheduler/image/result.pdf")
