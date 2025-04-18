import matplotlib.pyplot as plt


def plot(x):
    fig, ax = plt.subplots(figsize=(1, 1))
    ax.plot([x, x])
    ax.set_ylim(0, 3)
    ax.set_title(f"Plot {x}")
