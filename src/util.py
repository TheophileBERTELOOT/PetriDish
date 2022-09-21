def aColideWithB(x1,y1,radius,x2,y2):
    if x2<x1+radius and x2>x1-radius and y2<y1+radius and y2>y1-radius:
        return True
    else:
        return False