import argparse
from .profiling import profiling
from .fitting import fitting

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ASUSC Profiling")
    parser.add_argument("-i", "--image", type=str, required=True, help="image name")
    args = parser.parse_args()

    action = input("[+] Choose an action [profiling/fitting]: ")
    if action == "profiling":
        profiling(args.image)
    elif action == "fitting":
        fitting(args.image)
