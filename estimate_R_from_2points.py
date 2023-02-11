import matplotlib.pyplot as plt
import numpy as np
import plot_util
import calc_quatanion as cq


def estimate_R_from_2points():
    ax = plot_util.plot_base()

    # Plot originial 2 points
    ori_1 = np.array([1, 0, 1])
    ori_1_scalar = np.linalg.norm(ori_1)
    ori_1_norm = ori_1 / ori_1_scalar
    ori_2 = np.array([1, -1, 1])
    ori_2_scalar = np.linalg.norm(ori_2)
    ori_2_norm = ori_2 / ori_2_scalar
    ori_x = [ori_1_norm[0], ori_2_norm[0]]
    ori_y = [ori_1_norm[1], ori_2_norm[1]]
    ori_z = [ori_1_norm[2], ori_2_norm[2]]
    ax.scatter(ori_x, ori_y, ori_z, c='blue', alpha=0.4)

    U  = np.array([-0.1, -0.9, 0.2])     # unit vector (not normalized)
    Us = np.linalg.norm(U)               # scalar of U: |U|
    UV = U / Us
    print(UV)

    ori_quats = [np.insert(ori_1_norm, 0, 0), np.insert(ori_2_norm, 0, 0)]
    rotated_quats = [cq.QPQc(ori_q, UV, np.deg2rad(45)) for ori_q in ori_quats]
    rot_x = [rotated_quats[0][1:][0], rotated_quats[1][1:][0]]
    rot_y = [rotated_quats[0][1:][1], rotated_quats[1][1:][1]]
    rot_z = [rotated_quats[0][1:][2], rotated_quats[1][1:][2]]
    ax.scatter(rot_x, rot_y, rot_z, c='green', alpha=0.4)
    print(rotated_quats)
    print(rot_x)

    # Plot rotation axis vector
    ax.plot([0, UV[0]], [0, UV[1]], [0, UV[2]], c='r')
    ax.scatter(UV[0], UV[1], UV[2], c='r')
    ax.text(UV[0], UV[1], UV[2], s='  unit vector', va='top')

    # Plot rotated 2 points

    plt.show()


def main():
    estimate_R_from_2points()


if __name__ == '__main__':
    main()