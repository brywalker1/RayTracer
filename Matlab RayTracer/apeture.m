function [inregion, outregion] = apeture(rays, radius, center)
%apeture() sorts the rays, seperating those inside the sphere r = radius, c = center
%and those outside this region.  it Then returns both.
    temp = bsxfun(@minus,rays.position,[center,0]);
    in_region = dot(temp(:,1:3),temp(:,1:3),2) <= radius*radius;
    
    inregion  = mvrays(rays,in_region);
    outregion = mvrays(rays,not(in_region));
        
end
