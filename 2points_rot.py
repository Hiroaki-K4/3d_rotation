import matplotlib.pyplot as plt
import numpy as np


def QPQc(rot_axis_quat, ori_quat, rot_axis_conj_quat):

def main():
    A = np.array([1, -1, 1])             # initial vector A (arbitary vector)
    As = np.linalg.norm(A)               # scalar of A: |A|
    An = A / As                          # normalization: should be (sum(x**2 + y**2 + z**2))**0.5 = 1.0
    print("Initial vector: ", An)

    U  = np.array([-0.1, -0.9, 0.2])     # unit vector (not normalized)
    Us = np.linalg.norm(U)               # scalar of U: |U|
    UV = U / Us                          # unit vector (normalized)
    print("Rotation axis vector: ", UV)

    QA = np.insert(An, 0, 0)    # quaternion of An: [0, x, y, z]
    print(QA)
    theta = np.deg2rad(45)      # rotation angle
    print(theta)
    QB = QPQc(QA, UV, theta)
    print(QB)



if __name__ == '__main__':
    main()
