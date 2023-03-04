import matplotlib.pyplot as plt
import numpy as np
import plot_util
import calc_quatanion as cq
import random


DATA_NUMBER = 100

def estimate_R_with_isotropic_errors():
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

    ax.scatter(ori_x, ori_y, ori_z, c='blue', alpha=0.4)

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
    ax.scatter(rot_x, rot_y, rot_z, c='green', alpha=0.4)

    # Calculate R from 2 orthonormal systems.
    for i in range(DATA_NUMBER):
        dot = np.dot(ori_norm_list[i], rotated_quats[i].T)
        print("dot: ", dot)

    # N = ori_norm_list * rotated_quats.T
    # print("N: ", N)
    # print("ori_norm_list: ", ori_norm_list)

    plt.show()


if __name__ == '__main__':
    estimate_R_with_isotropic_errors()
