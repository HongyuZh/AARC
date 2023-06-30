from utils.container import Container
import argparse

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
    base_memory = 32
    sample = Container(args.container + ":v1", base_memory, 1)
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
