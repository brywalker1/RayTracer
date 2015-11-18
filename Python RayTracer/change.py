from rayTracer import Ray
#from rayTracer import unitVector
#import random
import numpy as np
s = np.sin(np.divide(0.0625,(-128,-64,-32,-16,-8,-4,-2,-1,np.inf,1,2,4,8,16,32,64,128)))
c = np.cos(np.divide(0.0625,(-128,-64,-32,-16,-8,-4,-2,-1,np.inf,1,2,4,8,16,32,64,128)))



def change(rays, changeRadius):


    x = np.random.randint(0,17);
    y = np.random.randint(0,17);
    z = np.random.randint(0,17);
    changeMat = np.array([  [            c[y]*c[z]      ,           -c[y]*s[z]      ,     s[y]  , 0],
                            [ c[x]*s[z] + c[z]*s[x]*s[y], c[x]*c[z] - s[x]*s[y]*s[z], -c[y]*s[x], 0],
                            [ s[x]*s[z] - c[x]*c[z]*s[y], c[z]*s[x] + c[x]*s[y]*s[z],  c[x]*c[y], 0],
                            [                0          ,                0          ,      0    , 1]  ]);

    numRays = rays.direction.shape[1];
    changeCentral = np.random.randint(0,numRays);
    
    #turns out, we want to change rays that are near each other, not far apart.
    shift2origin = rays.position - np.vstack(rays.position[:,changeCentral]);
    dist2 = np.sum(shift2origin*shift2origin, axis = 0);
    rays2Change = (dist2 <= changeRadius*changeRadius)

    rays.direction[:,rays2Change] = np.dot(changeMat, rays.direction[:,rays2Change]);
    
    return rays

"""Matrix Rotations:
   rotateX2 = [1   0   0   0;
               0   c[x] -s[x]  0;
               0   s[x]  c[x]  0;
               0   0   0   1];
   rotateY2 = [c[y]  0   s[y]  0;
               0   1   0   0;
              -s[y]  0   c[y]  0;
               0   0   0   1];
   rotateZ2 = [c[z] -s[z]  0   0;
               s[z]  c[z]  0   0;
               0   0   1   0;
               0   0   0   1];"""