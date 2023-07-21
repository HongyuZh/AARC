import pickle
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # recorders = []
    # for i in range(4):
    #     with open(f"path/path_{i}.pkl", "rb") as f:
    #         recorders.append(pickle.load(f))
    # for i, recorder in enumerate(recorders):
    #     fig, ax1 = plt.subplots()
    #     ax1.plot(recorder["runtime"], label="runtime", color="blue")
    #     ax1.axhline(recorder["SLO"], color="red", linestyle="dashed", label="SLO")
    #     ax1.set_ylabel("runtime")
    #     ax1.legend(loc="upper right")
    #     ax2 = ax1.twinx()
    #     ax2.plot(recorder["cost"], label="cost", color="green")
    #     ax2.set_ylabel("cost")
    #     ax2.legend(loc="upper center")
    #     plt.savefig(f"path_{i}.pdf")
    funcs = []
    for i in range(10):
        with open(f"func/fun_{i}.pkl", "rb") as f:
            funcs.append(pickle.load(f))
    for i, func in enumerate(funcs):
        fig, ax1 = plt.subplots()
        ax1.plot(func["cpu"], label="CPU", color="blue")
        ax1.set_ylabel("CPU")
        ax1.legend(loc="upper right")
        ax2 = ax1.twinx()
        ax2.plot(func["memory"], label="memory", color="green")
        ax2.set_ylabel("memory")
        ax2.legend(loc="upper center")
        plt.savefig(f"../image/schedule/func/func_{i}.pdf")
