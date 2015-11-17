import numpy as np
def propigate(rays, travel_distance):
    #%returns rays, after they have traveled travel_distance
    #%size(travel_distance) == 1 if all rays travel the same distance
    #%size(travel_distance,2)==size(rays.direction,2) if each ray travels a
    #%       unique distance
    #%note:  this function allows propigation to be negative
    #%note2: travel_distance is in millimeters I believe;
    #global visualize
    u = travel_distance * rays['direction'][:,0].T;
    v = travel_distance * rays['direction'][:,1].T;
    w = travel_distance * rays['direction'][:,2].T;
    
    #   this is for when I have time to add plotting functionality
    #    if bitand(visualize,2)
    #        x = rays.position(:,1);
    #        y = rays.position(:,2);
    #        z = rays.position(:,3);
    #        quiver3(x,y,z,u,v,w,0);
    #    end
    
    temp = np.array([u,v,w,u*0]).T;
    print(temp)
    rays['position'] = rays['position'] + temp; 
    print(rays['position']);
    #%take care of the phase propigation
    #vecMod =@(x,y) arrayfun(@(x,y) mod(x,y),x,y);

    numWaves = travel_distance/rays['wavelength']*10**6;#wavelength is in nanometers, position is in milimeters.
    newPhase = rays['phase'] + numWaves*rays['wavelength'];
    #%only want the fractions of wavelengths--whole sin waves repeat
    rays['phase'] = newPhase % rays['wavelength'];

    return rays;