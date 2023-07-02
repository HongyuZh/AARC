import pickle
import os

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def inverse_func(x, a, b):
    return a / x + b


def fitting(image_name):
    print(
        r"""
      _____.__  __    __  .__                
    _/ ____\__|/  |__/  |_|__| ____    ____  
    \   __\|  \   __\   __\  |/    \  / ___\ 
     |  |  |  ||  |  |  | |  |   |  \/ /_/  >
     |__|  |__||__|  |__| |__|___|  /\___  / 
                                  \//_____/  
    """
    )
    with open(f"profiling/data/profiling/{image_name}.pkl", "rb") as f:
        data = pickle.load(f)
    x = np.arange(0.25, 1.25, 0.25)
    y = np.array(data[:4])

    params_inverse, _ = curve_fit(inverse_func, x, y)
    a_inverse, b_inverse = params_inverse

    if not os.path.exists("profiling/data/fitting"):
        os.makedirs("profiling/data/fitting")
    with open(f"profiling/data/fitting/{image_name}.pkl", "wb") as f:
        pickle.dump(params_inverse, f)

    plt.figure()
    plt.scatter(x, y, label="Data")
    plt.plot(x, inverse_func(x, a_inverse, b_inverse), label="Inverse Fit")
    plt.legend()
    if not os.path.exists("profiling/image/fitting"):
        os.makedirs("profiling/image/fitting")
    plt.savefig(f"profiling/image/fitting/{image_name}.pdf")
    plt.close()

    with open("profiling/image/fitting/fitting.txt", "a") as file:
        file.write(f"{image_name}: y = {a_inverse} / x + {b_inverse}\n")
    print("[+] done")
