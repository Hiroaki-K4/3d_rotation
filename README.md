# 3d_rotation
Parameter computation and lie-Algebra based Optimization
<br></br>

## Rotate a point using quatanion
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
