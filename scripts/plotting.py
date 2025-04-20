import matplotlib.pyplot as plt
import numpy as np


def plot_sine(frequency=1):
    """Plot a sine wave with given frequency."""
    x = np.linspace(0, 10, 100)
    plt.figure(figsize=(2, 1.2))
    plt.plot(x, np.sin(frequency * x))
    plt.title(f"Sine Wave (f={frequency})")
    plt.ylim(-1.2, 1.2)


def plot_histogram(bins=20):
    """Plot a histogram of random data."""
    data = np.random.randn(1000)
    plt.figure(figsize=(2, 1.2))
    plt.hist(data, bins=bins)
    plt.title(f"Histogram (bins={bins})")
