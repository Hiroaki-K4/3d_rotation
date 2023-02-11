import matplotlib.pyplot as plt
import numpy as np
import plot_util
import calc_quatanion as cq


def plot_result(A, An, UV, B, Bn, arcx, arcy, arcz, As):
    ax = plot_util.plot_base()

    # Plot originial vector
    ax.plot([0, A[0]], [0, A[1]], [0, A[2]], c='b', alpha=0.4)
    ax.scatter(A[0], A[1], A[2], c='b', alpha=0.4)
    ax.text(A[0], A[1], A[2], s='  initial vector A', va='top')
    ax.plot([0, An[0]], [0, An[1]], [0, An[2]], c='b')
    ax.scatter(An[0], An[1], An[2], c='b')
    ax.text(An[0], An[1], An[2], s='  normalized vector An', va='top')

    # Plot rotation axis vector
    ax.plot([0, UV[0]], [0, UV[1]], [0, UV[2]], c='r')
    ax.scatter(UV[0], UV[1], UV[2], c='r')
    ax.text(UV[0], UV[1], UV[2], s='  unit vector', va='top')

    # Plot rotated vector
    ax.plot([0, B[0]], [0, B[1]], [0, B[2]], c='g', alpha=0.4)
    ax.text(B[0], B[1], B[2], s='initialized vector B  ', ha='right', va='top')
    ax.scatter(B[0], B[1], B[2], c='g', alpha=0.4)
    ax.plot([0, Bn[0]], [0, Bn[1]], [0, Bn[2]], c='g')
    ax.scatter(Bn[0], Bn[1], Bn[2], c='g')
    ax.text(Bn[0], Bn[1], Bn[2], s='normalized vector Bn  ', ha='right', va='top')

    # Plot rotation arc
    ax.plot(arcx, arcy, arcz, linestyle='--', c='b', alpha=0.6)
    ax.plot(arcx*As, arcy*As, arcz*As, linestyle='--', c='b', alpha=0.4)

    return ax


def main():
    A = np.array([1, -1, 1])             # initial vector A (arbitary vector)
    As = np.linalg.norm(A)               # scalar of A: |A|
    An = A / As                          # normalization: should be (sum(x**2 + y**2 + z**2))**0.5 = 1.0

    U  = np.array([-0.1, -0.9, 0.2])     # unit vector (not normalized)
    Us = np.linalg.norm(U)               # scalar of U: |U|
    UV = U / Us                          # unit vector (normalized)

    ori_q = np.insert(An, 0, 0)    # quaternion of An: [0, x, y, z]
    print("Original quatanion is: ", ori_q)
    theta = np.deg2rad(45)      # rotation angle
    rotated_q = cq.QPQc(ori_q, UV, theta)
    print("Rotated quatanion is: ", rotated_q)
    Bn = rotated_q[1:]
    B = Bn * As

    Arc = [cq.QPQc(ori_q, UV, t) for t in np.linspace(0, theta, 33)] # arc between A and B
    arcw, arcx, arcy, arcz = np.array(Arc).T

    plot_result(A, An, UV, B, Bn, arcx, arcy, arcz, As)
    plt.show()


if __name__ == '__main__':
    main()
