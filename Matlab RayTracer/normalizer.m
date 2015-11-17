function [NORMAL] = normalizer(VectorList)
%normalizer takes many vectors--arranged as consecutive columns in a matrix--and normalizes them 
    magnitude = sqrt(dot(VectorList,VectorList,2));
    magnitude(magnitude(:) == 0)=1;
    NORMAL = VectorList./[magnitude,magnitude,magnitude];
end

