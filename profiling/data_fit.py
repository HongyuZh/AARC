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
    for image in images:
        with open(f"data/{image}.pkl", "rb") as f:
            data = pickle.load(f)
        x = np.arange(0.25, 1.25, 0.25)
        y = np.array(data[:4])

        params_inverse, _ = curve_fit(inverse_func, x, y)
        a_inverse, b_inverse = params_inverse

        plt.scatter(x, y, label="Data")
        plt.plot(x, inverse_func(x, a_inverse, b_inverse), label="Inverse Fit")
        plt.legend()
        plt.savefig(f"data/{image}.pdf")
