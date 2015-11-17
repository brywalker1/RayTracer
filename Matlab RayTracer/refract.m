function [refracted,reflected] =  refract(rays, surfMatrix, n2)
%refract(rays, surfMatrix, n2)
%this function expects unit vectors to come in.
%the equation is based on a derivation in the book Introduction to Ray Tracing by glassner
n1 = rays.n_index;
rays.n_index(:) = n2;
r = n1./n2; %ratio
gradVec = getGrad(rays,surfMatrix);

 cos1 = dot(-rays.direction,gradVec,2);
 gradVec(cos1<0,:) = -gradVec(cos1<0,:);

cos1 = dot(rays.direction,gradVec,2);
cos2 = sqrt(1-r.*r.*(1-cos1.*cos1));  %if imaginary, there was internal reflection;
toRefl = imag(cos2)~=0;
cos1 = repmat(cos1,1,4); cos2 = repmat(cos2,1,4);
refl = rays.direction - 2*cos1.*gradVec;
rays.direction = repmat(r,1,4).*(rays.direction-cos1.*gradVec) - cos2.*gradVec;
rays.direction(toRefl,:) = refl(toRefl,:);

%I believe this is an unnecessary check to ensure that the result is
% %normalized; it is guaranteed to be normalized by the equation above.
% mag = sqrt(dot(rays.direction(1:3,:),rays.direction(1:3,:),1));
% mag(mag == 0) = 1;
% rays.direction(1:3,:) = rays.direction(1:3,:)./[mag;mag;mag];
% rays.direction(4,:) = 0;

%the 'rule of thumb' for phase reflections caused by refraction is:
%n1 to n2:  if high to low?  Phase shift no!
%           if low to high?  Phase shift pi!
if n1 < n2               % := phase + 'pi'
    rays.wavephase = rays.wavephase + rays.wavelength/2;
    %rays.wavephase = arrayfun(@(x,y) mod(x,y),rays.wavephase,rays.wavelength);
end

refracted = rays(not(toRefl),:);
reflected = rays(toRefl,:);
end