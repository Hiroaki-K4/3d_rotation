import matplotlib.pyplot as plt
import numpy as np
import plot_util
import calc_quatanion as cq
import random
from scipy.stats import random_correlation


DATA_NUMBER = 100


def estimate_R_with_isotropic_errors(ori_norm_arr, rotated_quats_arr):
    N = np.dot(ori_norm_arr.T, rotated_quats_arr)
    U, s, Vt = np.linalg.svd(N)
    V = Vt.T
    return np.dot(np.dot(V, np.diag([1, 1, np.linalg.det(V @ U)])), U.T)


def main():
    # Make noise
    cov_a = random_correlation.rvs((0.5, 1.2, 1.3))
    print(cov_a)
    cov_a_prime = random_correlation.rvs((0.1, 0.2, 2.7))
    print(cov_a_prime)
    np_mul = np.random.multivariate_normal(np.zeros(3), cov_a, 4)
    print("np_mul: ", np_mul)



if __name__ == '__main__':
    main()
