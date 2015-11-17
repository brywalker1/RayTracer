function [A, MinError] = bestFit()
n = .05;
a = .55;
L = 10;
dL = L*.1;
diff = 0; lastdiff= 1;
MinError = 100;
for i = .1:.1:1
    %figure out how what A fits a given range best;
    while(abs(diff-lastdiff) > 1e-5)
        [~,para,circ] = PnC(a,L,i);
        lastdiff = diff;
        diff = sum(circ(L/2-dL:L/2+dL)-para(L/2-dL:L/2+dL));
        if(diff>0)
            a = a+n;
        else
            a = a-n;
        end
        n = n/2;
    end
    if(diff < MinError)
        A = a;
        MinError = diff;
    end
end
end

function [ n,para,circ ] = PnC( A ,L, R)%Gain 
%plots a parabola, it's focal point, and the unit circle
%
n = -R:1/(L-.5):R;
circ = 1-sqrt(1-n.^2);
para = A.*(n.^2);

focus = zeros(1,size(n,2));
focus((size(n,2)/2)) = 1/(A*4);

%plot(n,circ,n,para,n,focus);
%pause(.25);
end

