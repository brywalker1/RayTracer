import numpy as np
#function [ grad ] = getGrad(rays,sM)
def getGrad(rays,sM):
    #%getGrad takes a surface and a list of rays already touching that surface,
    #%and returns the surface gradient vector at each point the rays are touching.
    #%sM stands for surface Matrix, I just wanted to keep the computations compact
    #%{    
    #  if your matrix coefficients are in a matrix as shown below,
    #        x     y    z    1   
    # x   | _x^2, 0   , 0  , 0 |
    # y   | _xy , _y^2, 0  , 0 |
    # z   | _xz , _yz ,_z^2, 0 |
    # 1   | _x  , _y  ,_z  ,_1 |

    #    Then taking the gradient of your equation returns the coefficients multiplied by:
    #  /            X                        Y                        Z          \    note: surf(i) is column-ordered 
    # |x   | _2x,   ,   ,   |   ,   |    ,   ,   ,   |   ,   |    ,   ,   ,   |  |          |  1  , 5 , 9 , 13 |
    # |y   | _y ,   ,   ,   |   ,   | _x ,_2y,   ,   |   ,   |    ,   ,   ,   |  |          |  2  , 6 ,10 , 14 |
    # |z   | _z ,   ,   ,   |   ,   |    ,_z ,   ,   |   ,   | _x ,_y ,_2z,   |  |          |  3  , 7 ,11 , 15 |
    # |1   | _1 ,   ,   ,   |   ,   |    ,_1 ,   ,   |   ,   |    ,   ,_1 ,   |  |          |  4  , 8 ,12 , 16 |
    #  \                                                                         /

    #For more information, check out
    #    https://www.cs.uaf.edu/2012/spring/cs481/section/0/lecture/01_26_ray_intersections.html
    #%}
    grad = np.dot(rays['position'],sM + sM.T); #and I think this one works even more efficiently.
    grad[:,3] = 0;

    #xr = rays['position'][:,0];
    #yr = rays['position'][:,1];
    #zr = rays['position'][:,2];
    
    ##dx = np.sum((sM[:,0] + np.transpose(sM[0,:]))*rays['position'] ,axis = 1); #I think this will work even better than the previous version (see below)
    #dx = 2*sM[0,0]*xr +   sM[1,0]*yr +   sM[2,0]*zr  + sM[3,0]  ;   
    #dy =   sM[1,0]*xr + 2*sM[1,1]*yr +   sM[2,1]*zr  + sM[3,1]  ;   
    #dz =   sM[2,0]*xr +   sM[2,1]*yr + 2*sM[2,2]*zr  + sM[3,2]  ;    
    #grad = np.vstack((dx,dy,dz,dz*0));
    
    mag = np.sqrt( np.sum((grad*grad),axis = 1))
    mag[mag == 0] = 1;
    grad = (grad.T/mag).T;
    grad[:,3] = 0;
    ##end
    return grad;