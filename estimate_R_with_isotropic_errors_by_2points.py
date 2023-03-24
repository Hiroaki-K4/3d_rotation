import matplotlib.pyplot as plt
import numpy as np
import plot_util
import calc_quatanion as cq


DATA_NUMBER = 5


def estimate_R_with_isotropic_errors(ori_norm_arr, rotated_quats_arr):
    N = np.dot(ori_norm_arr.T, rotated_quats_arr)
    U, s, Vt = np.linalg.svd(N)
    V = Vt.T
    R = np.dot(V, U.T)
    if np.linalg.det(R) < 0:
        V[:, 2] = -1 * V[:, 2]
        R = np.dot(V, U.T)

    return R


def main():
    ax = plot_util.plot_minimum()
    np.random.seed(10)

    # Prepare original data
    ori_x = []
    ori_y = []
    ori_z = []
    ori_list = []
    for i in range(DATA_NUMBER):
        ori_vec = np.array([np.random.uniform(-1,1), np.random.uniform(-1,1), np.random.uniform(0,1)])
        ori_list.append(ori_vec)

    ori_center = (ori_list[0] + ori_list[1]) / 2
    ori_vec_list = []
    for i in range(DATA_NUMBER):
        ori_vec = np.array([ori_list[i][0] - ori_center[0], ori_list[i][1] - ori_center[1], ori_list[i][2] - ori_center[2]])
        ori_x.append(ori_vec[0])
        ori_y.append(ori_vec[1])
        ori_z.append(ori_vec[2])
        ori_vec_list.append(ori_vec)

    ax.scatter(ori_x, ori_y, ori_z, c='green', alpha=0.4)

    U  = np.array([-0.1, -0.9, 0.2])     # unit vector (not normalized)
    Us = np.linalg.norm(U)               # scalar of U: |U|
    UV = U / Us
    # Plot rotation axis vector
    ax.plot([0, UV[0]], [0, UV[1]], [0, UV[2]], c='r')
    ax.scatter(UV[0], UV[1], UV[2], c='r')
    ax.text(UV[0], UV[1], UV[2], s='unit vector', va='top')

    # Prepare rotated data with isotropic error
    ori_quats = []
    for i in range(DATA_NUMBER):
        ori_quats.append(np.insert(ori_vec_list[i], 0, 0))
    rotated_quats = []

    i = 0
    for ori_q in ori_quats:
        noise = np.random.normal(0, 0.01, ori_vec.shape)
        print("noise: ", noise)
        rotated_quats.append(cq.QPQc(ori_q, UV, np.deg2rad(90))[1:] + noise)
        i += 1

    rot_x = []
    rot_y = []
    rot_z = []
    for i in range(DATA_NUMBER):
        rot_x.append(rotated_quats[i][0])
        rot_y.append(rotated_quats[i][1])
        rot_z.append(rotated_quats[i][2])
    ax.scatter(rot_x[:2], rot_y[:2], rot_z[:2], c='blue', alpha=1.0)
    ax.scatter(rot_x[2:], rot_y[2:], rot_z[2:], c='blue', alpha=0.3)

    # Calculate R from 2 orthonormal systems.
    ori_norm_arr = np.array(ori_vec_list)
    rotated_quats_arr = np.array(rotated_quats)

    R = estimate_R_with_isotropic_errors(ori_norm_arr[:2], rotated_quats_arr[:2])
    # R = estimate_R_with_isotropic_errors(ori_norm_arr[:5], rotated_quats_arr[:5])
    # R = estimate_R_with_isotropic_errors(ori_norm_arr, rotated_quats_arr)
    print(R)

    # Check if the estimated R is correct
    points_using_estimated_R = np.dot(R, ori_norm_arr.T)
    ax.scatter(points_using_estimated_R[0], points_using_estimated_R[1], points_using_estimated_R[2], c='red', alpha=0.4)

    dist = 0
    for i in range(DATA_NUMBER):
        dist += np.linalg.norm(rotated_quats_arr[i]-[points_using_estimated_R[0][i], points_using_estimated_R[1][i], points_using_estimated_R[2][i]])
    dist_avg = dist / DATA_NUMBER
    print("dist_avg: ", dist_avg)

    plt.show()


if __name__ == '__main__':
    main()
