function [ bins ] = makebins(rays,min,max,granularity)
%makebins divides the region of interest into small subsections, then
%counts the number of rays currently in each subsection.
%   The region of interest is a cartesian grid-aligned rectangular prism
%       bounded by min[x,y,z] and max[x,y,z]
%   granularity determines how fine the subregions should be (1 unit, .5
%       units, etc.)
%   rays is a list of the rays hopefully in the region.
%   This code has not been tested yet.
global visualize
x = min(1):granularity:max(1);
y = min(2):granularity:max(2);
z = min(3):granularity:max(3);
k = 1;
persistent timescalled;
if isempty(timescalled)
    timescalled = 1;
end
timescalled = timescalled + 1;
xscat = zeros(length(x)*length(y)*length(z),1);
yscat = xscat;
zscat = xscat;
num = xscat;
xpos = rays.position(:,1);
ypos = rays.position(:,2);
zpos = rays.position(:,3);
%preallocation
        for xi = 1:length(x)
            for yi = 1:length(y)
                for zi = 1:length(z)
                    %Do some binary & stuff, without multiplication, then
                    %count how many times it happens
                    num(k) = sum(  ( (xpos >= x(xi)) + (xpos < x(xi)+granularity) + ...
                                     (ypos >= y(yi)) + (ypos < y(yi)+granularity) + ...
                                     (zpos >= z(zi)) + (zpos < z(zi)+granularity) ) == 6); %all 6 statements are true;
                    if num(k) ~= 0
                        xscat(k) = x(xi);
                        yscat(k) = y(yi);
                        zscat(k) = z(zi);
                        k = k+1;
                    end
                end
            end
        end
        if bitand(visualize,1)                     
            scatter3(xscat,yscat,zscat,1+num*2,timescalled*16+zeros(size(xscat)));
        end
        bins = [xscat,yscat,zscat,num];
        bins(k:end,:) = []; %get rid of all those extra zeros
end