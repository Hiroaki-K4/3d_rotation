import matplotlib.pyplot as plt
import numpy as np
import plot_util
import calc_quatanion as cq
import random


DATA_NUMBER = 100


def estimate_R_with_isotropic_errors(ori_norm_arr, rotated_quats_arr):
    N = np.dot(ori_norm_arr.T, rotated_quats_arr)
    U, s, Vt = np.linalg.svd(N)
    V = Vt.T
    return np.dot(np.dot(V, np.diag([1, 1, np.linalg.det(V @ U)])), U.T)


def main():
    ax = plot_util.plot_base()
    random.seed(10)

    # Prepare original data
    ori_x = []
    ori_y = []
    ori_z = []
    ori_norm_list = []
    for i in range(DATA_NUMBER):
        ori_vec = np.array([random.random(), random.random(), random.random()])
        ori_scalar = np.linalg.norm(ori_vec)
        ori_norm = ori_vec / ori_scalar
        ori_x.append(ori_norm[0])
        ori_y.append(ori_norm[1])
        ori_z.append(ori_norm[2])
        ori_norm_list.append(ori_norm)

    ax.scatter(ori_x, ori_y, ori_z, c='green', alpha=0.4)

    U  = np.array([-0.1, -0.9, 0.2])     # unit vector (not normalized)
    Us = np.linalg.norm(U)               # scalar of U: |U|
    UV = U / Us
    # Plot rotation axis vector
    ax.plot([0, UV[0]], [0, UV[1]], [0, UV[2]], c='r')
    ax.scatter(UV[0], UV[1], UV[2], c='r')
    ax.text(UV[0], UV[1], UV[2], s='unit vector', va='top')

    # Make noise
    noise = np.random.normal(0, 3e-3, ori_norm.shape)

    # Prepare rotated data with isotropic error
    ori_quats = []
    for i in range(DATA_NUMBER):
        ori_quats.append(np.insert(ori_norm_list[i], 0, 0))
    rotated_quats = [cq.QPQc(ori_q, UV, np.deg2rad(90))[1:] + noise for ori_q in ori_quats]
    rot_x = []
    rot_y = []
    rot_z = []
    for i in range(DATA_NUMBER):
        rot_x.append(rotated_quats[i][0])
        rot_y.append(rotated_quats[i][1])
        rot_z.append(rotated_quats[i][2])
    ax.scatter(rot_x, rot_y, rot_z, c='blue', alpha=0.4)

    # Calculate R from 2 orthonormal systems.
    ori_norm_arr = np.array(ori_norm_list)
    rotated_quats_arr = np.array(rotated_quats)

    R = estimate_R_with_isotropic_errors(ori_norm_arr, rotated_quats_arr)

    # Check if the estimated R is correct
    points_using_estimated_R = np.dot(R, ori_norm_arr.T)
    ax.scatter(points_using_estimated_R[0], points_using_estimated_R[1], points_using_estimated_R[2], c='red', alpha=0.4)

    plt.show()


if __name__ == '__main__':
    main()
