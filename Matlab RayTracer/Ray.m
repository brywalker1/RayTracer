function [ray] = Ray(position, pointingToward,n_index)
%creates a single ray (or many rays)
%   position--where it is located [x1 y1 z1]
%   pointing toward--will combine with position to make a normalized
%   direction vector
%   n_index
   direction = pointingToward - position;
   mag = sqrt(dot(direction(:,1:3),direction(:,1:3),2));
   mag(mag==0) = 1;
   direction = direction./repmat(mag,1,size(direction,2));
   direction(:,4) = 0;
   position (:,4) = 1;
   
   n_index(1:size(direction)) = 1;%n_index;
   wavephase(1:size(direction)) = 0;%phase;
   wavelength(1:size(direction))= 600;%wavelength;
   
   %put the data in columns
   n_index   = n_index(:);
   wavephase = wavephase(:);
   wavelength= wavelength(:);
   
   ray = dataset(direction,position,n_index,wavelength,wavephase);
   
   
end