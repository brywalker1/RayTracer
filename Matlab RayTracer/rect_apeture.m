function [innerRays, outerRays] = rect_apeture(rays, min, max)
    
    in_region = (rays.position(1:3,:) > min) && (rays.position(1:3,:) < max);
    outerRays = rays(not(in_region));
    innerRays = rays(in_region);
end