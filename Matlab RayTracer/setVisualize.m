function setVisualize(num)
%setVisualize changes the global variable visualize for several functions
% svd  (dots surfaces vectors)
% 000 0 no visualizations should occur
% 001 1 dots only
% 010 2 vectors only
% 011 3 vectors and dots
% 100 4 surfaces only
% 101 5 surfaces and dots
% 110 6 vectors and surfaces
% 111 7 all should appear
global visualize
 visualize = num;
end