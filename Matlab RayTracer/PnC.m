function [ n,para,circ ] = PnC( A , L)
%plots a parabola, it's focal point, and the unit circle
%
n = -1:1/(L-.5):1;
circ = 1-sqrt(1-n.^2);
para = A.*(n.^2);

focus = zeros(1,size(n,2));
focus((size(n,2)/2)) = 1/(A*4);

plot(n,circ,n,para,n,focus);

end

