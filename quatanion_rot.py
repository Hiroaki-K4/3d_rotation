import matplotlib.pyplot as plt
import numpy as np


def QbyQ(q1, q2):
    w = q1[0]*q2[0] - q1[1]*q2[1] - q1[2]*q2[2] - q1[3]*q2[3]
    i = q1[0]*q2[1] + q1[1]*q2[0] + q1[2]*q2[3] - q1[3]*q2[2]
    j = q1[0]*q2[2] - q1[1]*q2[3] + q1[2]*q2[0] + q1[3]*q2[1]
    k = q1[0]*q2[3] + q1[1]*q2[2] - q1[2]*q2[1] + q1[3]*q2[0]
    return np.array([w, i, j, k])


def QPQc(ori_quat, rot_axis_quat, theta):
    q = [np.cos(theta/2), rot_axis_quat[0] * np.sin(theta/2), rot_axis_quat[1] * np.sin(theta/2), rot_axis_quat[2] * np.sin(theta/2)]
    qc = [np.cos(theta/2), -rot_axis_quat[0] * np.sin(theta/2), -rot_axis_quat[1] * np.sin(theta/2), -rot_axis_quat[2] * np.sin(theta/2)]
    qP = QbyQ(q, ori_quat)
    return QbyQ(qP, qc)


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
    return ax


def plot_result(A, An, UV, B, Bn, arcx, arcy, arcz, As):
    ax = plot_base()

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

    plt.show()


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
    rotated_q = QPQc(ori_q, UV, theta)
    print("Rotated quatanion is: ", rotated_q)
    Bn = rotated_q[1:]
    B = Bn * As

    Arc = [QPQc(ori_q, UV, t) for t in np.linspace(0, theta, 33)] # arc between A and B
    arcw, arcx, arcy, arcz = np.array(Arc).T

    plot_result(A, An, UV, B, Bn, arcx, arcy, arcz, As)


if __name__ == '__main__':
    main()
