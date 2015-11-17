function rays = big_source(min,max,direction, grain, n_index)
%big_source creates a large number of rays, spaced evenly from min to max, and going the same direction
%   This function is useful for creating things like parralel light rays
%   coming from infinity. Note that it creates a rectangular volume of
%   rays.  The region is grid aligned, but the vectors can point any direction
%       min = [xmin,ymin,zmin] a vector describing the min corner of the space
%       max = [xmax,ymax,zmax] a vector describing the max corner of the space
%       direction = [x,y,z] a cartesion description of where the vectors are pointing (will be normalized)
%       grain - how fine the spacing between rays is (ie .5 means there is a vector every .5 units in all directions)
%       n_index - describes material rays are passing through.  Air = 1.0-ish, water = 1.5-ish
direction = direction./norm(direction);
rays = struct('position',[0;0;0;0],'direction',[0;0;0;0],'n_index',n_index);
for i = min(1):grain:max(1)
    for j = min(2):grain:max(2)
        for k = min(3):grain:max(3)
        rays.position  = [rays.position, [i;j; k;1]];
        rays.direction = [rays.direction,[direction';0]];
        end
    end
end
end

