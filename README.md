# 3d_rotation
Parameter computation and lie-Algebra based Optimization
<br></br>

## **Rotate a point using quatanion**
In the image below, a quaternion is used to rotate a point.
```bash
python3 quatanion_rot.py
```
![quat](https://user-images.githubusercontent.com/51109408/217398841-5b6292c4-bba3-47a5-b3bf-a4f1763dae33.png)

### **How to calculate rotation using quatanion**
A is the point to move from now on.
```
A = [ax, ay, az]
```
Normalize A.
```
An = A / |A|
```
Unit vector: axis of rotation.
```
U = [ux, uy, uz]
```
Normalize U, if you need it.
```
Un = U / |U|
```
t is rotation angle.
```
t = θ
```
Substitute the angle and unit vector (rotational axis vector) in the following formula.
```
Q  = [cos(t/2),  ux*sin(t/2),  uy*sin(t/2),  uy*sin(t/2)]
Q- = [cos(t/2), -ux*sin(t/2), -uy*sin(t/2), -uy*sin(t/2)]
```
Calculate rotated quatanion using rotation fomula.
```
w, x, y, z = Q*A*Q-
```
The following formula is used for the multiplication of the above quaternions.
```
q1*q2 = [[q1w*q2w - q1x*q2x - q1y*q2y - q1z*q2z],
         [q1w*q2x + q1x*q2w + q1y*q2z - q1z*q2y],
         [q1w*q2y - q1x*q2z + q1y*q2w + q1z*q2x],
         [q1w*q2z + q1x*q2y - q1y*q2x + q1z*q2w]]
      = [w, x, y, z]
```
As a result, [w, x, y, z] is obtained, so extract only the xyz components and make it a vector.
```
[x, y, z]
```
If you want to return a scalar value that is equivalent to the vector before it was normalized, multiply it back by the original scalar value.
```
[x, y, z] * |A|
```

### **Reference**
- [クォータニオンと回転](https://www.f-sp.com/entry/2017/06/30/221124)
- [クォータニオン（四元数） / Quaternion / 回転制御（その１）](https://cnc-selfbuild.blogspot.com/2019/12/quaternion.html)
<br></br>

## **Calculate rotation matrix from 2points**
N vectors a1, ... , aN with rotation R, we obtain a'1, ... , a'N are obtained.
```
a'i = Ra,  i = 1,..,N
```
If there is no error in the data, two points are sufficient to find R.
As shown in the image below, the points ori1 and ori2 were rotated to create the points rot1 and rot2.
The method to find the Rotation matrix using ori1, ori2, rot1, rot2 is shown below.
![2points](https://user-images.githubusercontent.com/51109408/219936063-36f9c3e8-33e4-4bef-b346-2d2d0dc63718.png)

### **1. Find the outer product of two vectors and normalize it to a unit vector.**
The result obtained is **ori1*ori2** and **rot1*rot2** in the image below.
```
ori1*ori2 = Norm[ori1 × ori2]
rot1*rot2 = Norm[rot1 × rot2]
```
![cross1](https://user-images.githubusercontent.com/51109408/219935927-b02e5d3f-beaf-4cee-9b37-2f1ba2887dfc.png)

In addition, find the following outer products.
```
ori1*(ori1*ori2) = Norm[ori1 × (ori1 × ori2)]
rot1*(rot1*rot2) = Norm[rot1 × (rot1 × rot2)]
```
![cross2](https://user-images.githubusercontent.com/51109408/219935958-4d7a3b9f-181e-4259-a4d7-b3ddea1c474e.png)

### **2. Find Rotation matrix**
Calculate R1
```
r1 = Norm[ori1], r2 = Norm[ori1 × ori2], r3 = Norm[ori1 × (ori1 × ori2)]
R1 = (r1, r2, r3)
```
and calculate R2
```
r1' = Norm[rot1], r2' = Norm[rot1 × rot2], r3' = Norm[rot1 × (rot1 × rot2)]
R2 = (r1', r2', r3')
```
R1 and R2 are orthogonal matrices, mapping the basis {e1, e2, e3} to {r1, r2, r3} and {r1', r2', r3'} respectively. Thus, the following R maps {r1, r2, r3} to {r1', r2', r3'}. This R is the rotation matrix to be sought.
```
R = R2R1.T
```
![rotation](https://user-images.githubusercontent.com/51109408/219936558-c39616fb-4dce-4c67-b869-7897b2b04226.png)

The following commands can be used to perform a series of processes.
```bash
python3 estimate_R_from_2points.py
```

### **Reference**
- [3D Rotations: Parameter Computation and Lie-Algebra based Optimization chapter4](https://www.amazon.co.jp/3%E6%AC%A1%E5%85%83%E5%9B%9E%E8%BB%A2-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E8%A8%88%E7%AE%97%E3%81%A8%E3%83%AA%E3%83%BC%E4%BB%A3%E6%95%B0%E3%81%AB%E3%82%88%E3%82%8B%E6%9C%80%E9%81%A9%E5%8C%96-%E9%87%91%E8%B0%B7-%E5%81%A5%E4%B8%80/dp/4320113829)
<br></br>


## **How to estimate rotation matrix(If your data have isotropic errors)**
If there are errors in the data, the R to be sought is the R that minimizes the following J.

$$
J=\frac{1}{2}\sum_{\alpha=1}^N||a\prime_\alpha-Ra_\alpha||^2 ...(1)
$$

### **1. Solution by Singular Value Decomposition**
Expanding the expression gives

$$J=\frac{1}{2}\sum_{\alpha=1}^N\langle a\prime_\alpha-Ra_\alpha,a\prime_\alpha-Ra_\alpha \rangle$$

$$=\frac{1}{2}\sum_{\alpha=1}^N(\langle a\prime_\alpha,a\prime_\alpha \rangle-2\langle Ra_\alpha,a\prime_\alpha \rangle+\langle Ra_\alpha,Ra_\alpha \rangle)$$

$$=\frac{1}{2}\sum_{\alpha=1}^N||a\prime_\alpha||^2 -\sum_{\alpha=1}^N\langle Ra_\alpha,a\prime_\alpha \rangle+\frac{1}{2}\sum_{\alpha=1}^N||a_\alpha||^2...(2)$$

Therefore, to minimize this
$$K=\sum_{\alpha=1}^N\langle Ra_\alpha,a'_\alpha \rangle...(3)$$

You just need to calculate R that maximizes.
Using this,
$$\langle a,b \rangle=tr(ab^\intercal)...(4)$$

K can be written as follows. If you want to verify the above expression, run check_trace.py.  

$$K=tr(R\sum_{\alpha=1}^Na_\alpha a\prime_\alpha^\intercal)=tr(RN)...(5)$$

N was defined as follows.

$$N=\sum_{\alpha=1}^Na_\alpha a\prime_\alpha^\intercal...(6)$$

We show that the rotation R that maximizes equation (3) can be obtained by a singular value decomposition of N.

$$N=USV^\intercal...(7)$$

U, V are orthogonal matrices and S is a diagonal matrix such that.

$$S=diag(\sigma_1, \sigma_2, \sigma_3)$$

σ is is a large and small relationship as follows.

$$\sigma_1\geq\sigma_2\geq\sigma_3\geq0$$

Substituting (7) into equation (5), we obtain

$$K=tr(RUSV^\intercal)=tr(V^\intercal RUS)=tr(TS)...(8)$$

During the process, $tr(AB)=tr(BA)$ was used. And T was assumed

$$T=V^\intercal RU...(9)$$

Since U and V are orthogonal matrices and R is a rotation matrix (and thus an orthogonal matrix), T is also an orthogonal matrix. And if $T=(Tij)$, then

$$tr(TS)=tr\begin{pmatrix}
\begin{pmatrix}
T11 & T12 & T13 \\
T21 & T22 & T23 \\
T31 & T32 & T33 \\
\end{pmatrix}
\begin{pmatrix}
\sigma_1 & 0 & 0 \\
0 & \sigma_2 & 0 \\
0 & 0 & \sigma_3 \\
\end{pmatrix}
\end{pmatrix}$$

$$tr(TS)=tr
\begin{pmatrix}
\sigma_1T11 & \sigma_2T12 & \sigma_3T13 \\
\sigma_1T21 & \sigma_2T22 & \sigma_3T23 \\
\sigma_1T31 & \sigma_2T32 & \sigma_3T33 \\
\end{pmatrix}$$

$$=\sigma_1T11+\sigma_2T22+\sigma_3T33...(10)$$

Since an orthogonal matrix is a matrix with orthogonal unit vectors as rows and columns, no element has a size greater than 1. And since $\sigma_1,\sigma_2,\sigma_3\geq0$

$$tr(TS)\leq\sigma_1+\sigma_2+\sigma_3...(11)$$

The equal sign holds for $T11=T22=T33=1$, which implies $T=I$ Hence, if there exists a rotation R that makes T in equation (9) I, it is the rotation that maximizes K.
Let I be T in equation (9) and multiply by V from the left and U.T from the right, such that R,

$$R=VU^\intercal...(12)$$

If $|VU|(=|V||U|)=1$, $|R|=1$ and R is rotation matrix. Since V and U are orthogonal matrices, $|V|=\pm1$ and $|U|=\pm1$, but not necessarily $|VU|=1$.
When $T11=T22=T33=1$ cannot be achieved no matter how R is chosen, the following equation is true at the expense of the smallest $\sigma_3$.

$$tr(TS)\leq\sigma_1+\sigma_2-\sigma_3...(13)$$

The equal sign is formed by $T11=T22=1,T33=-1$. Since both rows and columns of T are orthonormal, this implies $T=diag(1,1,-1)$. Letting T in equation (9) be $diag(1,1,-1)$ and multiplying by $V$ from the left and $U^\intercal$ from the right, such that R

$$R=V\begin{pmatrix}
1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & -1 \\
\end{pmatrix}
U^\intercal...(14)$$

If $|VU=1|$, then $|R|=-1$, but if $|VU|=-1$, then $|R|=1$, where R is the rotation matrix.
From the above, the rotation matrix R that maximizes K, i.e., the least-squares solution R that minimizes Eq. (1), is given by combining Eqs. (12) and (14) as follows

$$R=V\begin{pmatrix}
1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & |VU| \\
\end{pmatrix}
U^\intercal...(15)$$

The following commands can be used to perform a series of processes.
```bash
python3 estimate_R_with_isotropic_errors.py
```

The blue point cloud in the image below is the green point cloud rotated by 90 degrees with the unit vector as the rotation axis, and isotropic error is added.

![ori_points](https://user-images.githubusercontent.com/51109408/222995663-6da32034-0617-4840-93d0-6a10a8236f64.png)

The red point cloud is a rotation of the green point cloud using the estimated R It overlaps the blue point cloud of the true value and is purple.

![test_data](https://user-images.githubusercontent.com/51109408/222995717-92daa9f5-0c5c-4fac-931f-58f13b558747.png)

### **2. Solution by quaternion representation**

$$q=q_0+q_1i+q_2j+q_3k...(16)$$

Using the above quaternion to denote R, we have

$$R=\begin{pmatrix}
q_0^2+q_1^2-q_2^2-q_3^2 & 2(q_1q_2-q_0q_3) & 2(q_1q_3+q_0q_2) \\
2(q_2q_1+q_0q_3) & q_0^2-q_1^2+q_2^2-q_3^2 & 2(q_2q_3-q_0q_1) \\
2(q_3q_1-q_0q_2) & 2(q_3q_2+q_0q_1) & q_0^2-q_1^2-q_2^2+q_3^2 \\
\end{pmatrix}...(17)$$

Using equation (17), $Ra_\alpha$ can be written as

$$Ra_\alpha=\begin{pmatrix}
(q_0^2+q_1^2-q_2^2-q_3^2)a_\alpha(1) + 2(q_1q_2-q_0q_3)a_\alpha(2) + 2(q_1q_3+q_0q_2)a_\alpha(3) \\
2(q_2q_1+q_0q_3)a_\alpha(1) + (q_0^2-q_1^2+q_2^2-q_3^2)a_\alpha(2) + 2(q_2q_3-q_0q_1)a_\alpha(3) \\
2(q_3q_1-q_0q_2)a_\alpha(1) + 2(q_3q_2+q_0q_1)a_\alpha(2) + (q_0^2-q_1^2-q_2^2+q_3^2)a_\alpha(3) \\
\end{pmatrix}$$

Hence, K in equation (3) can be written as

$$K=\sum_{\alpha=1}^N((q_0^2+q_1^2-q_2^2-q_3^2)a_\alpha(1)a\prime_\alpha(1)+2(q_1q_2-q_0q_3)a_\alpha(2)a\prime_\alpha(1) + 2(q_1q_3+q_0q_2)a_\alpha(3)a\prime_\alpha(1)$$

$$+2(q_2q_1+q_0q_3)a_\alpha(1)a\prime_\alpha(2)+(q_0^2-q_1^2+q_2^2-q_3^2)a_\alpha(2)a\prime_\alpha(2)+2(q_2q_3-q_0q_1)a_\alpha(3)a\prime_\alpha(2)$$

$$+2(q_3q_1-q_0q_2)a_\alpha(1)a\prime_\alpha(3)+2(q_3q_2+q_0q_1)a_\alpha(2)a\prime_\alpha(3)+(q_0^2-q_1^2-q_2^2+q_3^2)a_\alpha(3)a\prime_\alpha(3))$$

$$=\sum_{\alpha=1}^N(q_0^2(a_\alpha(1)a\prime_\alpha(1) + a_\alpha(2)a\prime_\alpha(2) + a_\alpha(3)a\prime_\alpha(3))$$
$$+q_1^2(a_\alpha(1)a\prime_\alpha(1) - a_\alpha(2)a\prime_\alpha(2) - a_\alpha(3)a\prime_\alpha(3))$$
$$+q_2^2(-a_\alpha(1)a\prime_\alpha(1) + a_\alpha(2)a\prime_\alpha(2) - a_\alpha(3)a\prime_\alpha(3))$$
$$+q_3^2(-a_\alpha(1)a\prime_\alpha(1) - a_\alpha(2)a\prime_\alpha(2) + a_\alpha(3)a\prime_\alpha(3))$$
$$+2q_0q_1(-a_\alpha(3)a\prime_\alpha(2) + a_\alpha(2)a\prime_\alpha(3)) + 2q_0q_2(a_\alpha(3)a\prime_\alpha(1) - a_\alpha(1)a\prime_\alpha(3))$$
$$+2q_0q_3(-a_\alpha(2)a\prime_\alpha(1) + a_\alpha(1)a\prime_\alpha(2)) + 2q_2q_3(a_\alpha(3)a\prime_\alpha(2) + a_\alpha(2)a\prime_\alpha(3))$$
$$+2q_3q_1(a_\alpha(3)a\prime_\alpha(1) + a_\alpha(1)a\prime_\alpha(3)) + 2q_1q_2(a_\alpha(2)a\prime_\alpha(1) + a_\alpha(1)a\prime_\alpha(2)))...(18)$$

Using the fact that the (i,j) elements of the correlation matrix N in equation (6) can be written as

$$Nij=\sum_{\alpha=1}^Na_\alpha(i) a\prime_\alpha(j)$$

the above equation can be written as follows

$$K=(q_0^2+q_1^2-q_2^2-q_3^2)N11+2(q_1q_2-q_0q_3)N21+2(q_1q_3+q_0q_2)N31$$
$$+2(q_2q_1+q_0q_3)N12+(q_0^2-q_1^2+q_2^2-q_3^2)N22+2(q_2q_3-q_0q_1)N32$$
$$+2(q_3q_1-q_0q_2)N13+2(q_3q_2+q_0q_1)N23+(q_0^2-q_1^2-q_2^2+q_3^2)N33$$
<br></br>
$$=q_0^2(N11+N22+N33)+q_1^2(N11-N22-N33)$$
$$+q_0^2(-N11+N22-N33)+q_0^2(-N11-N22+N33)$$
$$+2q_0q_1(-N32+N23)+2q_0q_2(N31-N13)$$
$$+2q_0q_3(-N21+N12)+2q_2q_3(N32+N23)$$
$$+2q_3q_1(N31+N13)+2q_1q_2(N21+N12)...(19)$$

Define a 4*4 symmetric matrix $N\prime$ as follows

$$N\prime=\begin{pmatrix}
N11+N22+N33 & -N32+N23 & N31-N13 & -N21+N12 \\
-N32+N23 & N11-N22-N33 & N21+N12 & N31+N13 \\
N31-N13 & N21+N12 & -N11+N22-N33 & N32+N23 \\
-N21+N12 & N31+N13 & N32+N23 & -N11-N22+N33
\end{pmatrix}...(20)$$

Using the 4-dimensional vector $q=(q_0,q_1,q_2,q_3)^\intercal$, equation (18) can be written as

$$K=\langle q,N\prime q \rangle...(21)$$

Since $N\prime$ is a symmetric matrix, from the Min-max theorem, q that maximizes Eq. (21) is the unit eigenvector for the largest eigenvalue of matrix $N\prime$. Substituting q into equation (17), we can determine R that maximizes K.

The following commands can be used to perform a series of processes.
```bash
python3 estimate_R_with_isotropic_errors_by_quaternion.py
```

### **Reference**
- [対称行列のレイリー商とは：最大・最小固有値との関係](https://math-fun.net/20210721/16543/)
