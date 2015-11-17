function [surf] = makeplane(normalVector,position)
%takes a vector normal to the surface of the plane and a position shift and
%returns the coefficients of the plane equation. also allows shorthand for
%the simplest plane equations: x = C, y = C, z = C
%google equation of a plane for more information
if ischar(normalVector)
    switch normalVector
        case {'x', 'X'}
            normalVector = [1,0,0];
        case {'y', 'Y'}
            normalVector = [0,1,0];
        case {'z', 'Z'}
            normalVector = [0,0,1];
        otherwise
            error('unrecognized input.  Please input either a gradient coefficients vector [a,b,c] or the character "x", "y", or "z", followed by a coordinate [x,y,z].');
    end
end
    x = position(1);
    y = position(2);
    z = position(3);
    a = normalVector(1);
    b = normalVector(2);
    c = normalVector(3);

    surf = [0 0 0 0;
            0 0 0 0;
            0 0 0 0;
            a b c -(a*x + b*y + c*z)];
end        