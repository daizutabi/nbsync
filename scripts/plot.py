import matplotlib.pyplot as plt
import numpy as np


def plot(func):
    x = np.linspace(0, 360)
    y = func(np.deg2rad(x))
    fig, ax = plt.subplots(figsize=(2, 1))
    ax.plot(x, y)
    ax.set_title(f"Plot {func.__name__}")


if __name__ == "__main__":
    # %% #sqrt
    plot(np.sqrt)
