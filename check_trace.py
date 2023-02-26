import numpy as np


def check_trace():
    A = np.array([[1,2,3],[4,5,6],[7,8,9]])
    B = np.array([[10,11,12],[13,14,15],[16,17,18]])
    print("A*B")
    print(A*B)
    AB_frobenius = np.sum(A*B)
    print("AB_frobenius: ", AB_frobenius)

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    AB_dot = np.dot(A, np.transpose(B))
    AB_trace = np.trace(AB_dot)
    print("AB_dot")
    print(np.dot(A, np.transpose(B)))
    print("AB_trace: ", AB_trace)


if __name__ == '__main__':
    check_trace()
