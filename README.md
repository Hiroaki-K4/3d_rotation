# 3d rotation
This repository is an experiment in understanding and experimenting with 3D rotation.  
Let's enjoy 3D rotation.
<br></br>

# Rotate a point using quatanion
In the image below, a quaternion is used to rotate a point.

```bash
python3 quatanion_rot.py
```

![quat](https://user-images.githubusercontent.com/51109408/217398841-5b6292c4-bba3-47a5-b3bf-a4f1763dae33.png)

## How to calculate rotation using quatanion
A is the point to move from now on.

$$
A = [ax, ay, az]
$$

Normalize A.

$$
A_n = \frac{A}{|A|}
$$

The following unit vector is the axis of rotation.

$$
U=[u_x, u_y, u_z]
$$

Normalize U, if you need it.

$$
U_n = \frac{U}{|U|}
$$

t is the rotation angle.

$$
t = θ
$$

Substitute the angle and unit vector (rotational axis vector) in the following formula.

$$
\begin{align*}
Q  &= [cos(t/2), u_x\times sin(t/2), u_y\times sin(t/2), u_y\times sin(t/2)] \\
Q^- &= [cos(t/2), -u_x\times sin(t/2), -u_y\times sin(t/2), -u_y\times sin(t/2)]
\end{align*}
$$

Calculate rotated quatanion using rotation fomula.

$$
w, x, y, z = QAQ^-
$$

The following formula is used for the multiplication of the above quaternions.

$$
q_1q_2=\begin{pmatrix}
w \\
x \\
y \\
z \\
\end{pmatrix}=\begin{pmatrix}
q_{1w}q_{2w}-q_{1x}q_{2x}-q_{1y}q_{2y}-q_{1z}q_{2z} \\
q_{1w}q_{2x}+q_{1x}q_{2w}+q_{1y}q_{2z}-q_{1z}q_{2y} \\
q_{1w}q_{2y}-q_{1x}q_{2z}+q_{1y}q_{2w}+q_{1z}q_{2x} \\
q_{1w}q_{2z}+q_{1x}q_{2y}-q_{1y}q_{2x}+q_{1z}q_{2w} \\
\end{pmatrix}
$$

As a result, [w, x, y, z] is obtained, so extract only the xyz components and make it a vector.  
If you want to return a scalar value that is equivalent to the vector before it was normalized, multiply it back by the original scalar value.

$$
\begin{pmatrix}
x \\
y \\
z \\
\end{pmatrix}\times |A|
$$

## References
- [クォータニオンと回転](https://www.f-sp.com/entry/2017/06/30/221124)
- [クォータニオン（四元数） / Quaternion / 回転制御（その１）](https://cnc-selfbuild.blogspot.com/2019/12/quaternion.html)

<br></br>

# Calculate rotation matrix from 2points
$N$ vectors $a_1, ... , a_N$ with rotation $R$, we obtain $a'_1, ... , a'_N$ are obtained.

$$
a\prime_i=Ra,  i=1,..,N
$$

If there is no error in the data, two points are sufficient to find $R$.
As shown in the image below, the points $ori1$ and $ori2$ were rotated to create the points $rot1$ and $rot2$.
The method to find the Rotation matrix using $ori1, ori2, rot1, rot2$ is shown below.

![2points](https://user-images.githubusercontent.com/51109408/219936063-36f9c3e8-33e4-4bef-b346-2d2d0dc63718.png)

## 1. Find the outer product of two vectors and normalize it to a unit vector.
The result obtained is **ori1*ori2** and **rot1*rot2** in the image below.

$$
ori_1*ori_2 = Norm[ori_1 × ori_2] \\
rot_1*rot_2 = Norm[rot_1 × rot_2]
$$

![cross1](https://user-images.githubusercontent.com/51109408/219935927-b02e5d3f-beaf-4cee-9b37-2f1ba2887dfc.png)

In addition, find the following outer products.

$$
ori_1*(ori_1*ori_2) = Norm[ori_1 × (ori_1 × ori_2)] \\
rot_1*(rot_1*rot_2) = Norm[rot_1 × (rot_1 × rot_2)]
$$

![cross2](https://user-images.githubusercontent.com/51109408/219935958-4d7a3b9f-181e-4259-a4d7-b3ddea1c474e.png)

## 2. Find Rotation matrix
Calculate $R_1$

$$
\begin{align*}
r_1 &= Norm[ori_1], \\
r_2 &= Norm[ori_1 × ori_2], \\
r_3 &= Norm[ori_1 × (ori_1 × ori_2)], \\
R_1&=\begin{pmatrix}
r_1 \\
r_2 \\
r_3\\
\end{pmatrix}
\end{align*}
$$

and calculate $R_2$

$$
\begin{align*}
r_1\prime &= Norm[rot_1], \\
r_2\prime &= Norm[rot_1 × rot_2], \\
r_3\prime &= Norm[rot_1 × (rot_1 × rot_2)], \\
R_2&=\begin{pmatrix}
r_1\prime \\
r_2\prime \\
r_3\prime \\
\end{pmatrix}
\end{align*}
$$

$R_1$ and $R_2$ are orthogonal matrices, mapping the basis $(e_1, e_2, e_3)$ to $(r_1, r_2, r_3)$ and $(r_1', r_2', r_3')$ respectively. Thus, the following $R$ maps $(r_1, r_2, r_3)$ to $(r_1', r_2', r_3')$. This R is the rotation matrix to be sought.

$$
R = R_2R_1^\intercal
$$

![rotation](https://user-images.githubusercontent.com/51109408/219936558-c39616fb-4dce-4c67-b869-7897b2b04226.png)

The following commands can be used to perform a series of processes.
```bash
python3 estimate_R_from_2points.py
```

<br></br>

## Reference
- [3D Rotations: Parameter Computation and Lie-Algebra based Optimization chapter4](https://www.amazon.co.jp/3%E6%AC%A1%E5%85%83%E5%9B%9E%E8%BB%A2-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E8%A8%88%E7%AE%97%E3%81%A8%E3%83%AA%E3%83%BC%E4%BB%A3%E6%95%B0%E3%81%AB%E3%82%88%E3%82%8B%E6%9C%80%E9%81%A9%E5%8C%96-%E9%87%91%E8%B0%B7-%E5%81%A5%E4%B8%80/dp/4320113829)

<br></br>

# How to estimate rotation matrix(If your data have isotropic errors)
If there are errors in the data, the $R$ to be sought is the $R$ that minimizes the following $J$.

$$
J=\frac{1}{2}\sum_{\alpha=1}^N||a\prime_\alpha-Ra_\alpha||^2 \tag{1}
$$

## 1. Solution by singular value decomposition
Expanding the expression gives

$$
\begin{align*}
J&=\frac{1}{2}\sum_{\alpha=1}^N\langle a\prime_\alpha-Ra_\alpha,a\prime_\alpha-Ra_\alpha \rangle \\

&=\frac{1}{2}\sum_{\alpha=1}^N(\langle a\prime_\alpha,a\prime_\alpha \rangle-2\langle Ra_\alpha,a\prime_\alpha \rangle+\langle Ra_\alpha,Ra_\alpha \rangle) \\

&=\frac{1}{2}\sum_{\alpha=1}^N||a\prime_\alpha||^2 -\sum_{\alpha=1}^N\langle Ra_\alpha,a\prime_\alpha \rangle+\frac{1}{2}\sum_{\alpha=1}^N||a_\alpha||^2 \tag{2}
\end{align*}
$$

Therefore, to minimize this

$$
K=\sum_{\alpha=1}^N\langle Ra_\alpha,a'_\alpha \rangle \tag{3}
$$

You just need to calculate $R$ that maximizes.
Using this,

$$
\langle a,b \rangle=tr(ab^\intercal) \tag{4}
$$

$K$ can be written as follows. If you want to verify the above expression, run **check_trace.py**.

$$
K=tr(R\sum_{\alpha=1}^Na_\alpha a\prime_\alpha^\intercal)=tr(RN) \tag{5}
$$

$N$ was defined as follows.

$$
N=\sum_{\alpha=1}^Na_\alpha a\prime_\alpha^\intercal \tag{6}
$$

We show that the rotation $R$ that maximizes equation (3) can be obtained by a singular value decomposition of $N$.

$$
N=USV^\intercal \tag{7}
$$

$U, V$ are orthogonal matrices and $S$ is a diagonal matrix such that.

$$
S=diag(\sigma_1, \sigma_2, \sigma_3)
$$

$\sigma$ is is a large and small relationship as follows.

$$
\sigma_1\geq\sigma_2\geq\sigma_3\geq0
$$

Substituting Eq(7) into Eq(5), we obtain

$$
K=tr(RUSV^\intercal)=tr(V^\intercal RUS)=tr(TS) \tag{8}
$$

During the process, $tr(AB)=tr(BA)$ was used. And $T$ was assumed

$$
T=V^\intercal RU \tag{9}
$$

Since $U$ and $V$ are orthogonal matrices and $R$ is a rotation matrix (and thus an orthogonal matrix), $T$ is also an orthogonal matrix. And if $T=(T_{ij})$, then

$$
\begin{align*}
tr(TS)
&=tr
\begin{pmatrix}
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
\end{pmatrix} \\

&=tr
\begin{pmatrix}
\sigma_1T11 & \sigma_2T12 & \sigma_3T13 \\
\sigma_1T21 & \sigma_2T22 & \sigma_3T23 \\
\sigma_1T31 & \sigma_2T32 & \sigma_3T33 \\
\end{pmatrix} \\

&=\sigma_1T11+\sigma_2T22+\sigma_3T33 \tag{10}
\end{align*}
$$

Since an orthogonal matrix is a matrix with orthogonal unit vectors as rows and columns, no element has a size greater than $1$. And since $\sigma_1,\sigma_2,\sigma_3\geq0$

$$tr(TS)\leq\sigma_1+\sigma_2+\sigma_3...(11)$$

The equal sign holds for $T_{11}=T_{22}=T_{33}=1$, which implies $T=I$. Hence, if there exists a rotation $R$ that makes $T$ in equation (9) $I$, it is the rotation that maximizes $K$.
Let $I$ be $T$ in equation (9) and multiply by $V$ from the left and $U^\intercal$ from the right, such that R,

$$
R=VU^\intercal \tag{12}
$$

If $|VU|(=|V||U|)=1$, $|R|=1$ and $R$ is rotation matrix. Since $V$ and $U$ are orthogonal matrices, $|V|=\pm1$ and $|U|=\pm1$, but not necessarily $|VU|=1$.
When $T11=T22=T33=1$ cannot be achieved no matter how $R$ is chosen, the following equation is true at the expense of the smallest $\sigma_3$.

$$
tr(TS)\leq\sigma_1+\sigma_2-\sigma_3 \tag{13}
$$

The equal sign is formed by $T_{11}=T_{22}=1,T_{33}=-1$. Since both rows and columns of $T$ are orthonormal, this implies $T=diag(1,1,-1)$. Letting $T$ in equation (9) be $diag(1,1,-1)$ and multiplying by $V$ from the left and $U^\intercal$ from the right, such that $R$

$$
R=V\begin{pmatrix}
1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & -1 \\
\end{pmatrix}
U^\intercal \tag{14}
$$

If $|VU|=1$, then $|R|=-1$, but if $|VU|=-1$, then $|R|=1$, where $R$ is the rotation matrix.
From the above, the rotation matrix $R$ that maximizes $K$, i.e., the least-squares solution $R$ that minimizes Eq. (1), is given by combining Eqs. (12) and (14) as follows

$$
R=V\begin{pmatrix}
1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & |VU| \\
\end{pmatrix}
U^\intercal \tag{15}
$$

The following commands can be used to perform a series of processes.

```bash
python3 estimate_R_with_isotropic_errors.py
```

The blue point cloud in the image below is the green point cloud rotated by $90$ degrees with the unit vector as the rotation axis, and isotropic error is added.

![ori_points](https://user-images.githubusercontent.com/51109408/222995663-6da32034-0617-4840-93d0-6a10a8236f64.png)

The red point cloud is a rotation of the green point cloud using the estimated $R$ It overlaps the blue point cloud of the true value and is purple.

![test_data](https://user-images.githubusercontent.com/51109408/222995717-92daa9f5-0c5c-4fac-931f-58f13b558747.png)
<br></br>

## 2. Solution by quaternion representation

$$
q=q_0+q_1i+q_2j+q_3k \tag{16}
$$

Using the above quaternion to denote $R$, we have

$$
R=\begin{pmatrix}
q_0^2+q_1^2-q_2^2-q_3^2 & 2(q_1q_2-q_0q_3) & 2(q_1q_3+q_0q_2) \\
2(q_2q_1+q_0q_3) & q_0^2-q_1^2+q_2^2-q_3^2 & 2(q_2q_3-q_0q_1) \\
2(q_3q_1-q_0q_2) & 2(q_3q_2+q_0q_1) & q_0^2-q_1^2-q_2^2+q_3^2 \\
\end{pmatrix} \tag{17}
$$

Using equation (17), $Ra_\alpha$ can be written as

$$Ra_\alpha=\begin{pmatrix}
(q_0^2+q_1^2-q_2^2-q_3^2)a_\alpha(1) + 2(q_1q_2-q_0q_3)a_\alpha(2) + 2(q_1q_3+q_0q_2)a_\alpha(3) \\
2(q_2q_1+q_0q_3)a_\alpha(1) + (q_0^2-q_1^2+q_2^2-q_3^2)a_\alpha(2) + 2(q_2q_3-q_0q_1)a_\alpha(3) \\
2(q_3q_1-q_0q_2)a_\alpha(1) + 2(q_3q_2+q_0q_1)a_\alpha(2) + (q_0^2-q_1^2-q_2^2+q_3^2)a_\alpha(3) \\
\end{pmatrix}$$

Hence, $K$ in equation (3) can be written as

$$
\begin{align*}
K=&\sum_{\alpha=1}^N((q_0^2+q_1^2-q_2^2-q_3^2)a_\alpha(1)a\prime_\alpha(1)+2(q_1q_2-q_0q_3)a_\alpha(2)a\prime_\alpha(1) + 2(q_1q_3+q_0q_2)a_\alpha(3)a\prime_\alpha(1) \\

&+2(q_2q_1+q_0q_3)a_\alpha(1)a\prime_\alpha(2)+(q_0^2-q_1^2+q_2^2-q_3^2)a_\alpha(2)a\prime_\alpha(2)+2(q_2q_3-q_0q_1)a_\alpha(3)a\prime_\alpha(2) \\

&+2(q_3q_1-q_0q_2)a_\alpha(1)a\prime_\alpha(3)+2(q_3q_2+q_0q_1)a_\alpha(2)a\prime_\alpha(3)+(q_0^2-q_1^2-q_2^2+q_3^2)a_\alpha(3)a\prime_\alpha(3)) \\

=&\sum_{\alpha=1}^N(q_0^2(a_\alpha(1)a\prime_\alpha(1) + a_\alpha(2)a\prime_\alpha(2) + a_\alpha(3)a\prime_\alpha(3)) \\

&+q_1^2(a_\alpha(1)a\prime_\alpha(1) - a_\alpha(2)a\prime_\alpha(2) - a_\alpha(3)a\prime_\alpha(3)) \\

&+q_2^2(-a_\alpha(1)a\prime_\alpha(1) + a_\alpha(2)a\prime_\alpha(2) - a_\alpha(3)a\prime_\alpha(3)) \\

&+q_3^2(-a_\alpha(1)a\prime_\alpha(1) - a_\alpha(2)a\prime_\alpha(2) + a_\alpha(3)a\prime_\alpha(3)) \\

&+2q_0q_1(-a_\alpha(3)a\prime_\alpha(2) + a_\alpha(2)a\prime_\alpha(3)) + 2q_0q_2(a_\alpha(3)a\prime_\alpha(1) - a_\alpha(1)a\prime_\alpha(3)) \\

&+2q_0q_3(-a_\alpha(2)a\prime_\alpha(1) + a_\alpha(1)a\prime_\alpha(2)) + 2q_2q_3(a_\alpha(3)a\prime_\alpha(2) + a_\alpha(2)a\prime_\alpha(3)) \\

&+2q_3q_1(a_\alpha(3)a\prime_\alpha(1) + a_\alpha(1)a\prime_\alpha(3)) + 2q_1q_2(a_\alpha(2)a\prime_\alpha(1) + a_\alpha(1)a\prime_\alpha(2))) \tag{18}
\end{align*}
$$

Using the fact that the $(i,j)$ elements of the correlation matrix $N$ in equation (6) can be written as

$$
N_{ij}=\sum_{\alpha=1}^Na_\alpha(i) a\prime_\alpha(j)
$$

the above equation can be written as follows

$$
\begin{align*}
K=&(q_0^2+q_1^2-q_2^2-q_3^2)N_{11}+2(q_1q_2-q_0q_3)N_{21}+2(q_1q_3+q_0q_2)N_{31} \\

&+2(q_2q_1+q_0q_3)N_{12}+(q_0^2-q_1^2+q_2^2-q_3^2)N_{22}+2(q_2q_3-q_0q_1)N_{32} \\

&+2(q_3q_1-q_0q_2)N_{13}+2(q_3q_2+q_0q_1)N_{23}+(q_0^2-q_1^2-q_2^2+q_3^2)N_{33} \\

=&q_0^2(N_{11}+N_{22}+N_{33})+q_1^2(N_{11}-N_{22}-N_{33}) \\

&+q_0^2(-N_{11}+N_{22}-N_{33})+q_0^2(-N_{11}-N_{22}+N_{33}) \\

&+2q_0q_1(-N_{32}+N_{23})+2q_0q_2(N_{31}-N_{13}) \\

&+2q_0q_3(-N_{21}+N_{12})+2q_2q_3(N_{32}+N_{23}) \\

&+2q_3q_1(N_{31}+N_{13})+2q_1q_2(N_{21}+N_{12}) \tag{19}
\end{align*}
$$

Define a $4\times 4$ symmetric matrix $N\prime$ as follows

$$
N\prime=
\begin{pmatrix}
N_{11}+N_{22}+N_{33} & -N_{32}+N_{23} & N_{31}-N_{13} & -N_{21}+N_{12} \\
-N_{32}+N_{23} & N_{11}-N_{22}-N_{33} & N_{21}+N_{12} & N_{31}+N_{13} \\
N_{31}-N_{13} & N_{21}+N_{12} & -N_{11}+N_{22}-N_{33} & N_{32}+N_{23} \\
-N_{21}+N_{12} & N_{31}+N_{13} & N_{32}+N_{23} & -N_{11}-N_{22}+N_{33}
\end{pmatrix} \tag{20}
$$

Using the $4$-dimensional vector $q=(q_0,q_1,q_2,q_3)^\intercal$, equation (19) can be written as

$$
K=\langle q,N\prime q \rangle \tag{21}
$$

Since $N\prime$ is a symmetric matrix, from the Min-max theorem, $q$ that maximizes Eq.(21) is the unit eigenvector for the largest eigenvalue of matrix $N\prime$. Substituting $q$ into equation (17), we can determine $R$ that maximizes $K$.

The following commands can be used to perform a series of processes.

```bash
python3 estimate_R_with_isotropic_errors_by_quaternion.py
```

<br></br>

## Reference
- [対称行列のレイリー商とは：最大・最小固有値との関係](https://math-fun.net/20210721/16543/)

<br></br>

## 3. Optimization of rotation matrix
$R$ estimated from image and sensor data may not be an exact rotation matrix due to errors.
We then consider the problem of correcting this to the exact rotation matrix $R$.
Specifically, the estimated $R\prime$ is replaced by the rotation matrix $R$ that minimizes $||R-R\prime||$.  
However, we define the matrix norm of the m*n matrix $A=(Aij)$ as

$$
||A||=\sqrt{\sum_{i=1}^m\sum_{j=1}^nAij^2} \tag{22}
$$

The following equation holds for the matrix norm in equation (22).

$$
||A||^2=tr(AA^\intercal)=tr(A^\intercal A)
$$

From this we can write $||R-R\prime||^2$ as

$$
\begin{align*}
||R-R\prime||^2&=tr((R-R\prime)(R-R\prime)^\intercal) \\

&=tr(RR^\intercal-RR\prime^\intercal-R\prime R^\intercal+R\prime R\prime^\intercal) \\

&=trI-tr(RR\prime^\intercal)-tr((RR\prime^\intercal)^\intercal)+tr(R\prime R\prime^\intercal) \\

&=3-2tr(RR\prime^\intercal)+||R\prime||^2
\end{align*}
$$

Therefore, the $R$ that minimizes $R-R\prime$ is the $R$ that maximizes $tr(RR\prime^\intercal)$. This is the same form as the maximization in Eq. (5).
Hence, the solution is determined by the singular value decomposition of $R\prime$.

$$
R\prime=USV^\intercal
$$

Since $R\prime^\intercal=USV^\intercal$, from equation (15) the solution is

$$
R=U
\begin{pmatrix}
1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & |UV| \\
\end{pmatrix}
V^\intercal
$$

The following commands can be used to perform a series of processes.

```bash
python3 optimize_R_matrix.py
```
