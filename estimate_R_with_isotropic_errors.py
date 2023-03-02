import matplotlib.pyplot as plt
import numpy as np
import plot_util
import calc_quatanion as cq
import random


def estimate_R_with_isotropic_errors():
    ax = plot_util.plot_base()
    random.seed(10)

    # Prepare original data
    ori_x = []
    ori_y = []
    ori_z = []
    ori_norm_list = []
    for i in range(100):
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
    # # Plot rotation axis vector
    ax.plot([0, UV[0]], [0, UV[1]], [0, UV[2]], c='r')
    ax.scatter(UV[0], UV[1], UV[2], c='r')
    ax.text(UV[0], UV[1], UV[2], s='unit vector', va='top')

    # Prepare rotated data
    ori_quats = []
    for i in range(100):
        ori_quats.append(np.insert(ori_norm_list[i], 0, 0))
    rotated_quats = [cq.QPQc(ori_q, UV, np.deg2rad(90)) for ori_q in ori_quats]
    rot_x = []
    rot_y = []
    rot_z = []
    for i in range(100):
        rot_x.append(rotated_quats[i][1:][0])
        rot_y.append(rotated_quats[i][1:][1])
        rot_z.append(rotated_quats[i][1:][2])
    ax.scatter(rot_x, rot_y, rot_z, c='green', alpha=0.4)

    # Calculate R from 2 orthonormal systems.
    # R1 = (r1, r2, r3), R2 = (r1', r2', r3') -> R = R2R1T(transpose)
    # R1 = np.array([ori_1_norm, ori_cross_pro_norm, ori_cross_pro_2_norm]).T
    # R2 = np.array([rotated_quats[0][1:], rot_cross_pro_norm, rot_cross_pro_2_norm]).T
    # R = np.dot(R2, R1.T)
    # print("R: ", R)
    # rot_1_from_R = np.dot(R, ori_1_norm)
    # rot_2_from_R = np.dot(R, ori_2_norm)
    # if np.allclose(rot_1_from_R, rotated_quats[0][1:]) and np.allclose(rot_2_from_R, rotated_quats[1][1:]):
    #     print("R Estimation from 2points is succeed!!")
    # else:
    #     print("R Estimation from 2points is failed!!")

    plt.show()


if __name__ == '__main__':
    estimate_R_with_isotropic_errors()
