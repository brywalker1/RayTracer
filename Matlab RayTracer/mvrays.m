function [rays] =  mvrays(rays, indx)
%mvrays allows select a specific set of rays in a group and return just them
% for example mvrays(rays, rays.n_index > 3) would return only the sets in
% the variable rays for which the n_index is greater than three,
% eliminating the rest
    rays = rays(indx,:);
end

