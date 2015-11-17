import numpy as np
from getGrad import getGrad
from hitAndmiss import hitAndMiss


#function [refracted,reflected] =  refract(rays, surfMatrix, n2)
def refract(rays, surfMatrix, n2 = 1):
#%refract(rays, surfMatrix, n2)
#%this function expects unit vectors to come in.
#%the equation is based on a derivation in the book Introduction to Ray Tracing by glassner
    r = rays['n_index']/n2; #ratio n1/n2
    rays['n_index'][:] = n2;
    gradVec = getGrad(rays,surfMatrix);

    cos1 = np.sum(-rays['direction']*gradVec,axis = 1);
    gradVec[cos1<0,:] = -gradVec[cos1<0,:];

    cos1 = np.sum(-rays['direction']*gradVec,axis = 1);
    cos2 = np.lib.scimath.sqrt(1-r*r*(1-cos1*cos1));  #%if imaginary, there was internal reflection;
    toRefl = cos2.imag != 0;
    #cos1 = repmat(cos1,1,4); cos2 = repmat(cos2,1,4);
    refl = rays['direction'] - (2*cos1*gradVec.T).T;
    rays['direction'] = (r * ((rays['direction']-(cos1*gradVec.T).T) - (cos2*gradVec.T).T).T).T;#refract these rays
    rays['direction'][:,toRefl] = refl[:,toRefl];#reflect these rays

    #%I believe this is an unnecessary check to ensure that the result is
    #% %normalized; it is guaranteed to be normalized by the equation above.
    #% mag = sqrt(dot(rays.direction(1:3,:),rays.direction(1:3,:),1));
    #% mag(mag == 0) = 1;
    #% rays.direction(1:3,:) = rays.direction(1:3,:)./[mag;mag;mag];
    #% rays.direction(4,:) = 0;

    #%the 'rule of thumb' for phase reflections caused by refraction is:
    #%n1 to n2:  if high to low?  Phase shift no!
    #%           if low to high?  Phase shift pi!
    if n1 < n2:                #% := phase + 'pi'
        rays['phase'] = (rays['phase'] + rays['wavelength']/2) % rays['wavelength'];
    #    %rays.wavephase = arrayfun(@(x,y) mod(x,y),rays.wavephase,rays.wavelength);
    #end
    reflected, refracted = hitAndMiss(rays, toRefl);
    
    return refracted;