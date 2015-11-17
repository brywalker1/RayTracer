import numpy as np

def makePlane(normalVector,position):
    #%takes a vector normal to the surface of the plane and a position shift and
    #%returns the coefficients of the plane equation. also allows shorthand for
    #%the simplest plane equations: x = C, y = C, z = C
    #%google equation of a plane for more information
    
    if type(normalVector) == type('a'):
        normalVector = {
            'x': np.array([1,0,0],float),
            'X': np.array([1,0,0],float),
            'y': np.array([0,1,0],float),
            'Y': np.array([0,1,0],float),
            'z': np.array([0,0,1],float),
            'Z': np.array([0,0,1],float),
            }[normalVector]
    
        x = position[0];
        y = position[1];
        z = position[2];
        a = normalVector[0];
        b = normalVector[1];
        c = normalVector[2];

        surf = np.array([[0, 0, 0, 0], 
                         [0, 0, 0, 0], 
                         [0, 0, 0, 0], 
                         [a, b, c, -(a*x + b*y + c*z)] ],float);

    return surf