function [C] = addM(A,B)
%matrix helper function--adds the x,y,z,etc parts of a vector to the
%x,y,z,etc rows of a matrix.
C = zeros(size(B));
for i = 1:size(B,2)
    C(:,i) = A(:,i) + B(:,i);
end
end