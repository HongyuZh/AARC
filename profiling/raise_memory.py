import os
import pickle
import numpy as np
from colorama import Fore
from utils.container import Container
from utils.plot import plot_two_lines


def raise_memory(image_name):
    print(
        r"""
                  .__                                        
    ____________  |__| ______ ____     _____   ____   _____  
    \_  __ \__  \ |  |/  ___// __ \   /     \_/ __ \ /     \ 
     |  | \// __ \|  |\___ \\  ___/  |  Y Y  \  ___/|  Y Y  \
     |__|  (____  /__/____  >\___  > |__|_|  /\___  >__|_|  /
                \/        \/     \/        \/     \/      \/     
    """
    )
    sample = Container(image_name, 1024, 0.25)
    sample.run()
    for i in range(3):
        sample.updateAllocation(cpu=sample.cpu + 0.25)
        sample.run()
    sample.delete()
    sample.display()

    # plot
    with open(f"profiling/data/profiling/{image_name}.pkl", "rb") as f:
        base_data = pickle.load(f)
    data = [recorder[2] for recorder in sample.recorder[-4:]]
    if not os.path.exists("profiling/image/raise_memory"):
        os.mkdir("profiling/image/raise_memory")
    plot_two_lines(
        fig_name=f"{image_name}",
        xticks=np.arange(0, 4),
        xiticklabels=np.arange(0.25, 1.25, 0.25),
        xlabel="CPU(s)",
        y1lim=(0, (max(data) // 1000 + 2.5) * 1000),
        y1label="Latency (ms)",
        y2lim=(0, 2),
        y2label="Proportion",
        values1=data,
        label1="Raise memory",
        values2=[now / base for now, base in zip(data, base_data[:4])],
        label2="Comparison",
        path="profiling/image/raise_memory",
    )
