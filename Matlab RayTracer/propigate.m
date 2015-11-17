function [rays] = propigate(rays, travel_distance)
%returns rays, after they have traveled travel_distance
%size(travel_distance) == 1 if all rays travel the same distance
%size(travel_distance,2)==size(rays.direction,2) if each ray travels a
%       unique distance
%note:  this function allows propigation to be negative
%note2: travel_distance is in meters;    
global visualize
    u = travel_distance .* rays.direction(:,1);
    v = travel_distance .* rays.direction(:,2);
    w = travel_distance .* rays.direction(:,3);
    
    if bitand(visualize,2)
        x = rays.position(:,1);
        y = rays.position(:,2);
        z = rays.position(:,3);
        quiver3(x,y,z,u,v,w,0);
    end
rays.position = rays.position + [u,v,w,u.*0]; 

%take care of the phase propigation
vecMod =@(x,y) arrayfun(@(x,y) mod(x,y),x,y);

numWaves = travel_distance./rays.wavelength.*10^9;
newPhase = rays.wavephase + numWaves.*rays.wavelength;
%only want the fractions of wavelengths--whole sin waves repeat
rays.wavephase(:) = vecMod(newPhase,rays.wavelength);

end