import numpy as np
from propigate import propigate
from hitAndmiss import hitAndMiss
def get2surf(rays, surfMatrix):
#function [rays, missRays] = get2surf(rays, surfMatrix)
#%get2surf(rays, surfMatrix) takes an array of rays, and determines if and when they will intersect the surface described by surfMatrix.
#%   %a lot of thanks go to
#%   https://www.cs.uaf.edu/2012/spring/cs481/section/0/lecture/01_26_ray_intersections.html,
#%   but the simple version is that a ray is defined as a vector [A + tB],
#%   where A and B are known vectors like [1,2,0] + t*[3,1.5,2]
#%   and a surface is defined as an equation in xyz, like 3x + y - z = 0.
#%   We combine the two equations, solve for t, and that is how far the
#%   vector must travel to reach its destination.
#    global visualize;
    surfD = np.zeros_like(rays['direction']);
    surfP = surfD.copy();

    #for i in range(rays[direction].shape[1]) = 1:size(rays.direction,1)
    surfD = np.dot(rays['direction'] , surfMatrix) ;
    surfP = np.dot(rays['position' ] , surfMatrix) ;
    
    a = np.sum(surfD * rays['direction'],axis = 1);                                             #a*t^2
    b = np.sum(surfD * rays['position' ],axis = 1) + np.sum(surfP*rays['direction'],axis = 1);  #b*t
    c = np.sum(surfP * rays['position' ],axis = 1);                                             #c*1

    t = np.zeros_like(a);
    #distRoot = np.array([np.zeros_like(a),np.zeros_like(b)],float );
    #for indx in range(len(a)):
    #    distRoot[indx,:] = np.roots([a[indx],b[indx],c[indx]]);

    #   now we are going to solve for what t is for each equation. There are several cases, so we update them as we cover them.
    #   First check if there actually is an a*t^2 component -- if not, our math is easy x = -c/b
    badCase = np.array([np.inf],float); #if we didn't intersect by the time we traveled to infinity
    up = np.abs(a) < .0001;
    t[up] = -c[up]/b[up];
    
    #now for those weird cases when there wasn't an a or a b-->aka there is no intersection. Mark these cases
    t[up & (np.abs(b) < .001)] = badCase;


    #now for the regular case--we don't need to update the previous sets anymore
    up = ~up;

    #for the regular case, use the quadratic formula: x = (-b +- sqrt(b^2-4ac)) / 2a
    # sqrtQuad = sqrt(b^2-4ac)
    sqrtQuad = np.sqrt(b[up]*b[up]-4*a[up]*c[up]);
   
    temp1 = (-b[up] + sqrtQuad);
    temp1[[any(bad) for bad in np.array((temp1.imag !=0, temp1.real <= 0)).T]] = badCase;
   
    temp2 = (-b[up] - sqrtQuad);
    temp2[[any(bad) for bad in np.array((temp2.imag !=0, temp2.real <= 0)).T]] = badCase;

    t[up] = np.min([temp1,temp2],axis = 0);
    #if t.count(badCase):
    #    isMiss = t.index(badCase);
    #else:
    #    isMiss = np.array([]);
    isHit = (t != badCase);
    (hitRays, missRays) = hitAndMiss(rays,isHit);
    t = t[isHit];

    hitRays = propigate(hitRays,t);
    return (hitRays,missRays);
#    missRays = rays(isMiss,:);    %return these just in case someone wants to do something with them anyways.
#    rays = rays(not(isMiss),:);   %in this context, the imaginary rays are rays that miss our object, and are removed;
#    rays = propigate(rays, t(not(isMiss)));
#    if bitand(visualize,4)
#        showSurface(rays);
#    end
#end
