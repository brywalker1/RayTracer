import numpy as np
def makeCircle(radius, center_coordinates):
    #function [ circ ] = makecircle(radius, center_coordinates)
    #% makes a spherical surface, also explains the process of making any
    #% surface
    x1 = center_coordinates[0];
    y1 = center_coordinates[1];
    z1 = center_coordinates[2];
    #%{
    #  The hardest thing about using this system is understanding the matrix
    #    format.  The first step is to determine the equation of your surface.
    #    For a sphere of radius r, centered at point (x1,y1,z1), the equation is
    
    #        (x-x1)^2 + (y-y1)^2 + (z-z1)^2 = r^2.

    #    Multiply everything out, move everything to the right side, and set = 0
    
    #(1)x^2 + (1)y^2 + (1)z^2 + (-2*x1)x + (-2*y1)y + (-2*z1)z + (x1^2 + y1^2 + z1^2 - r^2) = 0

    #We now place our coefficients into a matrix of the form shown below.  For
    #example, __x^2 would be replaced by 1, the x^2 coefficient
    #        x     y    z    1   
    # x   | _x^2, 0   , 0  , 0 |
    # y   | _xy , _y^2, 0  , 0 |
    # z   | _xz , _yz ,_z^2, 0 |
    # 1   | _x  , _y  ,_z  ,_1 |

    #For more information, check out
    #    https://www.cs.uaf.edu/2012/spring/cs481/section/0/lecture/01_26_ray_intersections.html
    #%}
    circ = np.array([[ 1,    0,    0,    0],
                     [ 0,    1,    0,    0],
                     [ 0,    0,    1,    0],
                     [-2*x1,-2*y1,-2*z1,(x1*x1+y1*y1+z1*z1-radius*radius)]]);
    
    return circ;  
    #%To create quadriatic shapes other than circles, derive the equation, and
    #%fill in the coefficient matrix.
    #end