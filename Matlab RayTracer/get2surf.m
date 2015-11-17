function [rays, missRays] = get2surf(rays, surfMatrix)
%get2surf(rays, surfMatrix) takes an array of rays, and determines if and when they will intersect the surface described by surfMatrix.
%   %a lot of thanks go to
%   https://www.cs.uaf.edu/2012/spring/cs481/section/0/lecture/01_26_ray_intersections.html,
%   but the simple version is that a ray is defined as a vector [A + tB],
%   where A and B are known vectors like [1,2,0] + t*[3,1.5,2]
%   and a surface is defined as an equation in xyz, like 3x + y - z = 0.
%   We combine the two equations, solve for t, and that is how far the
%   vector must travel to reach its destination.
    global visualize;
    surfD = sym(zeros(size(rays.direction)));
    surfP = surfD;
    surfMatrix = sym(surfMatrix);
    for i = 1:size(rays.direction,1)
        surfD(i,:) = surfMatrix*rays.direction(i,:).';
        surfP(i,:) = surfMatrix*rays.position (i,:).'; 
    end
    a = dot(rays.direction,surfD,2);                                  % a*t^2
    b = dot(rays.position ,surfD,2) + dot(rays.direction, surfP,2);   % b*t
    c = dot(rays.position ,surfP,2);                                  % c*1
    
    t = arrayfun( @(a,b,c) least_positive(a,b,c),a,b,c);   % t = (-b +- sqrt(b^2 - 4ac))/2a
    
    isMiss = (imag(t) ~= 0) | t < 0;   %to also exclude points that are already at surface check t <= 0 instead
    missRays = rays(isMiss,:);    %return these just in case someone wants to do something with them anyways.
    rays = rays(not(isMiss),:);   %in this context, the imaginary rays are rays that miss our object, and are removed;
    rays = propigate(rays, t(not(isMiss)));
    if bitand(visualize,4)
        showSurface(rays);
    end
end

function posMin = least_positive(a,b,c)
   %  solves the equation a*t^2 + b*t + c == 0 and returns the smallest
   %  positive solution.
    if abs(a) < .0001 %if a == 0
        if abs(b) < .0001 %if b == 0
            vec = [];
        else
         vec = eval(-c/b);
        end
   else
       vec(1) = eval((-b + sqrt(b*b-4*a*c))/(2*a));
       vec(2) = eval((-b - sqrt(b*b-4*a*c))/(2*a));
   end
   if size(vec,1) == 0
       vec(1) = 99i;
   end
   if(imag(vec(1)))
       posMin = vec(1);
   else
       posMin = vec(vec >= 0);
       if min(size(posMin)) == 0
           posMin = max(vec);
       else
           posMin = min(posMin);
       end
   end
end
