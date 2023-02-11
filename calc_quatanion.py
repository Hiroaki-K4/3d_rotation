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
