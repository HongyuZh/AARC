from .profiling import profiling
from .fitting import fitting
from .raise_memory import raise_memory
from colorama import Fore

if __name__ == "__main__":
    images = [
        "chameleon:v1",
        "float_operation:v1",
        "matmul:v1",
        "model_serving:v1",
        "pyaes:v1",
    ]
    action = input(
        "[+] Choose an action [p for profiling/f for fitting/r for raising memory/e for exit]: "
    )

    if action == "p":
        for image in images:
            profiling(image)
    elif action == "f":
        for image in images:
            fitting(image)
    elif action == "r":
        for image in images:
            raise_memory(image)
    elif action == "e":
        exit(0)
    else:
        print(f"{Fore.RED}[ERROR]{Fore.RESET} Invalid action, exit...")
        exit(1)
