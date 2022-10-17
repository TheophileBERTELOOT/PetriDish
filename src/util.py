import numpy as np
def aColideWithB(x1,y1,radius,x2,y2):
    if x2<x1+radius and x2>x1-radius and y2<y1+radius and y2>y1-radius:
        return True
    else:
        return False

def lineColideWithCircle(L,E,C,r):
    d = L - E
    f = E - C
    r = r*2
    a = d.dot(d)
    b = 2 * f.dot(d)
    c = f.dot(f) - r ** 2
    discriminant = b * b - 4 * a * c
    if discriminant >= 0:
        discriminant = np.sqrt(discriminant);
        t1 = (-b - discriminant) / (2 * a)
        t2 = (-b + discriminant) / (2 * a)
        if t1 >= 0 and t1 <= 1:
            return True
        if t2 >=0 and t2 <=1:
            return True
    return False

def  calcDistanceBetweenTwoPoint(p1,p2):
    return np.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)