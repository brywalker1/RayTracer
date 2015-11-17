plane = makeplane('z',[0,0,0]);
figure;
%% pick the depth
depth_of_bot = 1.9
%     try
syms x y z;
surf = funct2surf(.1*(x^2 + y^2) - z - depth_of_bot);
lens = funct2surf(-.05*(x^2+y^2) - z - .03);%-.05*(x^2=y^2)-z - .05
% depth_of_bot = 1.5;
surf = makecircle(5,[0, 0, 5-depth_of_bot]);%(3,[00,3-1.1]) is interesting as well
% surf = makeplane('z',[0,0,-depth_of_bot]);



radius = .75;%.75

% x = radius*sin(pi/3:pi/3:2*pi); x = x(:);
% y = radius*cos(pi/3:pi/3:2*pi); y = y(:);
% z = zeros(size(x));             z = z(:);
% extra = z;
% 
% goingto = [x(:),y(:),z(:),extra(:)];
% scatter3(x(:),y(:),z(:)+depth_of_bot);
% hold on;
% scatter3(x(:)*5,y(:)*5,z(:)+depth_of_bot);
% 
% toppoint = [x(:),y(:),extra(:)+5,extra(:)].';
% % point = repmat(point,size(goingto,1),1);
% stepDegrees = 5;
% 
%     %% go for it
%     for theta = (15:stepDegrees:80)/180*pi+.01;
% 
%     s = sin(theta);
%     c = cos(theta);
% 
%     rotateX = [1  0  0  0;
%                0  c -s  0;
%                0  s  c  0;
%                0  0  0  1];
%     rotateY = [c  0  s  0;
%                0  1  0  0;
%               -s  0  c  0;
%                0  0  0  1];
%     rotateZ = [c -s  0  0;
%                s  c  0  0;
%                0  0  1  0;
%                0  0  0  1];
    position = [1,0,0];
    scatter3(position(1),position(2),position(3)+1);
    rays = point_source(position,1);%(rotateX*toppoint).';
    hold on;
    %scatter3(point(:,1),point(:,2),point(:,3));
    %rays = Ray(point,goingto,1);
    %rays = get2surf(rays,plane);
    %rays = apeture(rays,radius,[0,0,0]);
    setVisualize(7);
    rays = rays(rays.direction(:,3)<0,:);%shooting downwards
    rays = get2surf(rays,surf);
    rays = reflect(rays,surf);
    rays = get2surf(rays,lens);
    rays = apeture(rays,radius,[0,0,0]);
    rays = refract(rays,lens,1.5);
    rays = get2surf(rays,plane);
    rays = refract(rays,plane,1.0);
    rays = propigate(rays,5);
    showSurface(rays);
    drawnow;
%     end
%     catch
%     end
% end