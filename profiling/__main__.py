import argparse
import pickle
import json

import numpy as np
from utils.container import Container
from utils.plot import plot_lines

if __name__ == "__main__":
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
    parser = argparse.ArgumentParser(description="ASUSC Profiling")
    parser.add_argument(
        "-c", "--container", type=str, required=True, help="container name"
    )
    args = parser.parse_args()

    # find base memory
    sample = Container(args.container, 32, 1)
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

    # profiling
    sample.updateAllocation(cpu=0.25)
    sample.run(autodelete=True)
    for i in range(7):
        sample.updateAllocation(cpu=sample.cpu + 0.25)
        sample.run(autodelete=True)
    sample.delete()
    sample.display(save=True)

    # plot
    data = [recorder[2] for recorder in sample.recorder[-8:]]
    plot_lines(
        fig_name=sample.image_id,
        xticks=np.arange(0, 8),
        xiticklabels=np.arange(0.25, 2.25, 0.25),
        xlabel="CPU(s)",
        ylim=(0, (max(data) // 1000 + 2.5) * 1000),
        ylabel="Latency (ms)",
        values_list=[np.array(data)],
        labels=["CPU"],
        path="profiling/image",
    )

    with open("profiling/data/" + sample.image_id + ".pkl", "wb") as f:
        pickle.dump([recorder[2] for recorder in sample.recorder[-8:]], f)
