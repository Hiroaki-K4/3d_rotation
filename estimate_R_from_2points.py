import matplotlib.pyplot as plt
import numpy as np


def plot_base(elev=25, azim=-70):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.view_init(elev=elev, azim=azim)
    ax.set(xlim=(-1, 1), ylim=(-1 ,1), zlim=(-1, 1))
    ax.set(xlabel='X', ylabel='Y', zlabel='Z')
    ax.xaxis.pane.fill = ax.yaxis.pane.fill = ax.zaxis.pane.fill = False

    t = np.linspace(0, 2*np.pi, 128+1)
    alpha = 0.7
    # Plot arc
    ax.plot(np.cos(t), np.sin(t), [0]*len(t), linestyle=':', c='red', alpha=alpha)
    ax.plot(np.cos(t), [0]*len(t), np.sin(t), linestyle=':', c='red', alpha=alpha)
    ax.plot([0]*len(t), np.cos(t), np.sin(t), linestyle=':', c='red', alpha=alpha)
    # Plot axis
    ax.plot([-1, 1], [0, 0], [0, 0], linestyle=':', c='red', alpha=alpha)
    ax.plot([0, 0], [-1, 1], [0, 0], linestyle=':', c='red', alpha=alpha)
    ax.plot([0, 0], [0, 0], [-1, 1], linestyle=':', c='red', alpha=alpha)
    plt.show()
    return ax


def main():

    plot_base()


if __name__ == '__main__':
    main()