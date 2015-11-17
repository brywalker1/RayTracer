function [rays] = point_source(varargin)
%point_source(position, n_index,granularity)
%load or create a point source, emitting rays in all directions.
    wavelength = 600;%nm--yellow light
    position = cell2mat(varargin(1));
    granularity = 5;%bigger = more rays
    n_index = 1;
    phase = 0; %what phase the lightWave is in
    if(nargin > 1),  n_index = cell2mat(varargin(2));  end
    if(nargin > 2),  granularity = floor(cell2mat(varargin(3))); end  %must be int

    try
        load fine_point_source
    catch
        %x^2 + y^2 + z^2 = 1
        x2(granularity*granularity) = 0;
        y = zeros(size(x2));
        z = zeros(size(x2));
        k = 1;
        sine = 0:1/(granularity - 1):1;
        sine = sin(pi.*sine./2);
        for yindx = 1:granularity
            for zindx = 1:granularity
                y(k)  = sine(yindx);
                z(k)  = sine(zindx);
                x2(k) = 1-sine(yindx)*sine(yindx)-sine(zindx)*sine(zindx);
                k = k + 1;
            end
        end
        toKeep = not(x2 < 0);
        x = sqrt(x2)  ;
        x = x(toKeep); % x = [x,-x]
        y = y(toKeep); % y = [y,=y]
        z = z(toKeep); % z = [z,-z]
        direction(:,1) = [ x, x, x, x,-x,-x,-x,-x].';
        direction(:,2) = [ y, y,-y,-y, y, y,-y,-y].';
        direction(:,3) = [ z,-z, z,-z, z,-z, z,-z].';
        direction = normalizer(direction);
        direction(:,4) = 0;
        rays = dataset(direction);
        save fine_point_source rays
    end %try to load a point source. if that fails, make one.
    mposition = zeros(size(rays.direction));%matrix position;
    mposition(:,1) = position(1);
    mposition(:,2) = position(2);
    mposition(:,3) = position(3);
    mposition(:,4) = 1;
    rays.position = mposition;
    rays.n_index(1) = n_index;
    rays.wavelength(1) = wavelength;
    rays.wavephase(1) = 0; %in units of wavelength, not 2pi
    
    rays.n_index(:) = n_index;
    rays.wavelength(:) = wavelength;
    rays.wavephase(:) = phase;
    rays.Properties.Units = {'m' '' '' 'nm' 'nm'};
    
end