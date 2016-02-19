"""
Utilities for linear algebra

We only care 3D:
  * vectors are lists of length 3
  * matrices are 3-by-3 lists of lists
"""

import math


class Vector(list):
    def norm(u):
        return math.sqrt(u.dot(u))

    def dot(u, v):
        """Dot product"""
        u1, u2, u3 = u
        v1, v2, v3 = v
        return math.fsum([u1*v1, u2*v2, u3*v3])

    def cross(u, v):
        """Cross product"""
        u1, u2, u3 = u
        v1, v2, v3 = v
        return Vector([
            u2*v3 - u3*v2,
            u3*v1 - u1*v3,
            u1*v2 - u2*v1,
        ])

    def angle(u, v):
        """Angle formed by two vectors"""
        r = u.dot(v)/u.norm()/v.norm()
        r = max(-1, min(1, r))
        return math.acos(r)

    def oriented_angle(u, v, normal=None):
        """Angle formed by two vectors"""
        if normal is None:
            normal = Vector([0, 0, 1])
        geometric_angle = u.angle(v)
        if normal.dot(u.cross(v)) < 0:
            return -geometric_angle
        else:
            return geometric_angle

    def __mul__(u, s):
        x, y, z = u
        return Vector([x*s, y*s, z*s])

    def __div__(u, s):
        x, y, z = u
        return Vector([x/s, y/s, z/s])

    def __add__(u, v):
        x, y, z = u
        a, b, c = v
        return Vector([x+a, y+b, z+c])

    def __iadd__(u, v):
        x, y, z = u
        a, b, c = v
        return Vector([x+a, y+b, z+c])

    def __sub__(u, v):
        x, y, z = u
        a, b, c = v
        return Vector([x-a, y-b, z-c])

    def __isub__(u, v):
        x, y, z = u
        a, b, c = v
        return Vector([x-a, y-b, z-c])

    def __neg__(u):
        x, y, z = u
        return Vector([-x, -y, -z])

    def __abs__(u):
        """Maximum metric (see Chebyshev distance)"""
        return max(u)


class Matrix(list):
    def __sub__(A, B):
        return Matrix([x-y for a, b in zip(A, B) for x, y in zip(a, b)])

    def __abs__(A):
        """Maximum metric (see Chebyshev distance)"""
        return max(abs(a) for a in A)

    def __mul__(self, x):
        if isinstance(x, Matrix):  # matrix-matrix multiplication
            m = Matrix(zip(*x))
            return Matrix([m*row for row in self])
        else:  # matrix-vector multiplication
            # 3x3 version (optimized)
            [a, b, c], [d, e, f], [g, h, i] = self
            x, y, z = x
            return Vector([
                a*x + b*y + c*z,
                d*x + e*y + f*z,
                g*x + h*y + i*z,
            ])
            # generic version
            # return Vector([sum(a*b for a, b in zip(row, x)) for row in self])

    @classmethod
    def identity(cls):
        return cls([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    @classmethod
    def rotation(cls, angle, x, y, z):
        """Rotation matrix of given angle (radians) around axis (x,y,z)"""
        s = math.sin(angle)
        c = math.cos(angle)
        d = math.sqrt(x*x + y*y + z*z)
        x, y, z = x/d, y/d, z/d
        return cls([
            [x*x*(1-c)+c,   x*y*(1-c)-z*s, x*z*(1-c)+y*s],
            [y*x*(1-c)+z*s, y*y*(1-c)+c,   y*z*(1-c)-x*s],
            [z*x*(1-c)-y*s, z*y*(1-c)+x*s, z*z*(1-c)+c],
        ])

    @classmethod
    def from_euler_angles(cls, alpha, beta, gamma):
        """Return the rotation matrix from the given Z1X2Z3 Euler angles"""
        # see https://en.wikipedia.org/wiki/Euler_angles#Rotation_matrix
        c1, s1 = math.cos(alpha), math.sin(alpha)
        c2, s2 = math.cos(beta),  math.sin(beta)
        c3, s3 = math.cos(gamma), math.sin(gamma)
        return cls([
            [c1*c3-c2*s1*s3, -c1*s3-c2*c3*s1, s1*s2],
            [c3*s1+c1*c2*s3, c1*c2*c3-s1*s3,  -c1*s2],
            [s2*s3,          c3*s2,           c2],
        ])

    @classmethod
    def rotation_deg(cls, angle, x, y, z):
        """Rotation matrix of given angle (degrees) around axis (x,y,z)"""
        return cls.rotation(math.radians(angle), x, y, z)
