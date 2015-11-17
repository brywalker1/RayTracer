function rays = reflect(rays, surfMatrix)
%reflect takes vectors hitting a surface, and returns them just after being reflected
%   there are two important requirements:
%       The rays must have already reached the surface
%       their direction vector must be toward the surface.
    gradVec = getGrad(rays, surfMatrix);
    for i = 1:size(rays.direction,1)
        rays.direction(i,1:4) = rays.direction(i,1:4)-2*dot(rays.direction(i,1:4),gradVec(i,1:4))*gradVec(i,1:4);
    end
    %mirrors cause a pi phase shift in the wave phase:
    rays.wavephase = rays.wavephase + rays.wavelength/2;
    rays.wavephase = arrayfun(@(x,y) mod(x,y),rays.wavephase,rays.wavelength);
end
