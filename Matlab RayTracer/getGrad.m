function [ grad ] = getGrad(rays,sM)
%getGrad takes a surface and a list of rays already touching that surface,
%and returns the surface gradient vector at each point the rays are touching.
%sM stands for surface Matrix, I just wanted to keep the computations compact
%{    
  if your matrix coefficients are in a matrix as shown below,
        x     y    z    1   
 x   | _x^2, 0   , 0  , 0 |
 y   | _xy , _y^2, 0  , 0 |
 z   | _xz , _yz ,_z^2, 0 |
 1   | _x  , _y  ,_z  ,_1 |

    Then taking the gradient of your equation returns the coefficients multiplied by:
  /            X                        Y                        Z          \    note: surf(i) is column-ordered 
 |x   | _2x,   ,   ,   |   ,   |    ,   ,   ,   |   ,   |    ,   ,   ,   |  |          |  1  , 5 , 9 , 13 |
 |y   | _y ,   ,   ,   |   ,   | _x ,_2y,   ,   |   ,   |    ,   ,   ,   |  |          |  2  , 6 ,10 , 14 |
 |z   | _z ,   ,   ,   |   ,   |    ,_z ,   ,   |   ,   | _x ,_y ,_2z,   |  |          |  3  , 7 ,11 , 15 |
 |1   | _1 ,   ,   ,   |   ,   |    ,_1 ,   ,   |   ,   |    ,   ,_1 ,   |  |          |  4  , 8 ,12 , 16 |
  \                                                                         /

For more information, check out
    https://www.cs.uaf.edu/2012/spring/cs481/section/0/lecture/01_26_ray_intersections.html
%}
    xr = rays.position(:,1);
    yr = rays.position(:,2);
    zr = rays.position(:,3);
    
    dx = 2*sM(1).*xr +   sM(2).*yr +   sM(3).*zr  + sM(4)  ;   
    dy =   sM(2).*xr + 2*sM(6).*yr +   sM(7).*zr  + sM(8)  ;   
    dz =   sM(3).*xr +   sM(7).*yr + 2*sM(11).*zr + sM(12) ;    
    grad = [dx,dy,dz];
    
    mag = sqrt(dot(grad,grad,2));
    mag(mag == 0) = 1;
    grad = grad./[mag,mag,mag];
    grad(end,4) = 0;
end