function surf = fucnt2surf(equation)
%given: Ax^2 + Bx + Cy^2 + Dy + Ez^2 +Fz + Gxy + Hyz + Izx + constant = 0
%find:  A,B,C,D,E,F,G,H,I,constant
syms x y z
f(x,y,z) = equation;

%syms x y z
%f(x,y,z) = x^2 + 3*x + x*y + 4*y*y + 5*y + 2* z + 7;

%the constant in the equation
const = f(0,0,0);

%determine the x stuff
i2 = f(1,0,0); %answer when x = 1
i3 = f(2,0,0); %answer when x = 2
A = (i3-2*i2+const)/2;
B =  i2-const-A;

%determine the y stuff
j2 = f(0,1,0); %answer when x = 1
j3 = f(0,2,0); %answer when x = 2
C = (j3-2*j2+const)/2;
D =  j2-const-C;

%determine the y stuff
k2 = f(0,0,1); %answer when x = 1
k3 = f(0,0,2); %answer when x = 2
E = (k3-2*k2+const)/2;
F =  k2-const-E;

G = f(1,1,0) - f(0,1,0) - f(1,0,0) + const;
H = f(0,1,1) - f(0,1,0) - f(0,0,1) + const;
I = f(1,0,1) - f(1,0,0) - f(0,0,1) + const;
        

             % x   y   z   1
surf = eval([  A , 0 , 0 , 0 ;     % x
               G , C , 0 , 0 ;     % y
               I , H , E , 0 ;     % z
               B , D , F , const]);% 1
end