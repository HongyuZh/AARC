import pickle
import json
import os

import numpy as np
from colorama import Fore
from utils.container import Container
from utils.plot import plot_lines


def profiling(image_name):
    print(
        r"""
                         _____.__.__  .__                
    _____________  _____/ ____\__|  | |__| ____    ____  
    \____ \_  __ \/  _ \   __\|  |  | |  |/    \  / ___\ 
    |  |_> >  | \(  <_> )  |  |  |  |_|  |   |  \/ /_/  >
    |   __/|__|   \____/|__|  |__|____/__|___|  /\___  / 
    |__|                                      \//_____/   
    """
    )
    # find base memory
    sample = Container(image_name, 32, 1)
    with open("profiling/config/config.json", "r") as f:
        config = json.load(f)
    if sample.image_id in config:
        base_memory = config[sample.image_id]
        sample.updateAllocation(memory=base_memory)
    else:
        base_memory = 32
        while True:
            try:
                sample.run()
            except:
                base_memory += 32
                sample.updateAllocation(memory=base_memory)
                continue
            break
        print(f"[+] Base memory is {base_memory} MB")
        with open("profiling/config/config.json", "w") as f:
            config[sample.image_id] = base_memory
            json.dump(config, f, indent=4)

    # profiling
    sample.updateAllocation(cpu=0.25)
    try:
        sample.run(autodelete=True)
    except:
        print(
            f"{Fore.YELLOW}[!]{Fore.RESET} Running failed using the config in profiling/config/config.json, please check it"
        )
        exit(1)
    for i in range(7):
        sample.updateAllocation(cpu=sample.cpu + 0.25)
        sample.run(autodelete=True)
    sample.delete()
    sample.display()

    # plot
    data = [recorder[2] for recorder in sample.recorder[-8:]]
    plot_lines(
        fig_name=sample.image_id,
        xticks=np.arange(0, 8),
        xiticklabels=np.arange(1, 9),
        xlabel="CPU(s)",
        ylim=(0, (max(data) // 1000 + 2.5) * 1000),
        ylabel="Latency (ms)",
        values_list=[np.array(data)],
        labels=["CPU"],
        path="profiling/image/profiling",
    )

    if not os.path.exists("profiling/data/profiling"):
        os.makedirs("profiling/data/profiling")
    with open("profiling/data/profiling/" + sample.image_id + ".pkl", "wb") as f:
        pickle.dump([recorder[2] for recorder in sample.recorder[-8:]], f)
