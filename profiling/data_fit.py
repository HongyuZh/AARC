import pickle

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def inverse_func(x, a, b):
    return a / x + b


if __name__ == "__main__":
    images = [
        "chameleon:v1",
        "float_operation:v1",
        "matmul:v1",
        "model_serving:v1",
        "pyaes:v1",
    ]
    file = open("fitting/fitting.txt", "w")
    for image in images:
        with open(f"data/{image}.pkl", "rb") as f:
            data = pickle.load(f)
        x = np.arange(0.25, 1.25, 0.25)
        y = np.array(data[:4])

        params_inverse, _ = curve_fit(inverse_func, x, y)
        a_inverse, b_inverse = params_inverse

        with open(f"data/{image}_fitting.pkl", "wb") as f:
            pickle.dump(params_inverse, f)

        plt.figure()
        plt.scatter(x, y, label="Data")
        plt.plot(x, inverse_func(x, a_inverse, b_inverse), label="Inverse Fit")
        plt.legend()
        plt.savefig(f"fitting/{image}.pdf")
        plt.close()

        file.write(f"{image}: y = {a_inverse} / x + {b_inverse}\n")
    file.close()
