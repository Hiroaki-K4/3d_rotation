# 3d_rotation
Parameter computation and lie-Algebra based Optimization
<br></br>

## **Rotate a point using quatanion**
In the image below, a quaternion is used to rotate a point.
```
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

## **Estimate Rotation matrix from 2points**
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

The following commands can be used to perform a series of processes.
```
python3 estimate_R_from_2points.py
```

### **Reference**
- [3D Rotations: Parameter Computation and Lie-Algebra based Optimization chapter4](https://www.amazon.co.jp/3%E6%AC%A1%E5%85%83%E5%9B%9E%E8%BB%A2-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E8%A8%88%E7%AE%97%E3%81%A8%E3%83%AA%E3%83%BC%E4%BB%A3%E6%95%B0%E3%81%AB%E3%82%88%E3%82%8B%E6%9C%80%E9%81%A9%E5%8C%96-%E9%87%91%E8%B0%B7-%E5%81%A5%E4%B8%80/dp/4320113829)
