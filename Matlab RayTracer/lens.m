function rays = lens(varargin) %n1 is already in rays.
%lens(rays,surf1,n2,[surf2,n3])
%   This function has not been tested.
    rays = varargin{1};
    surf1= varargin{2};
    n2   = varargin{3};
    n1 = rays.n_index;
    
    rays = get2surf(rays,surf1);
    rays = refract(rays,surf1,n2);
    
    if nargin == 3 %if this is a thin lens
        rays.n_index = n1; %then we are back in air;
    else
        surf2= varargin{4};
        
        if nargin == 5 %if n1 ~= n3. (if we are entering a 3rd, new material)
            n3=varargin{5}; 
        else
            n3 = rays.n_index;
        end
        
        rays = get2surf(rays,surf2);
        rays = refract(rays,surf2,n3);
    end
