import copy
import numpy as np

def unitVector(rays):
        mag = np.sqrt( np.sum((rays[0:3,:]*rays[0:3,:]),axis = 0))
        mag[mag == 0] = 1;
        rays[0:3,:] = rays[0:3,:]/mag;
        return rays

def Ray(position, pointingToward, n_index = 1, phase = 0, wavelength = 600):
    #a safe wrapper to make a ray with--if something goes wrong, return None instead of a ray set
    try:
        return lightRay(position,pointingToward, n_index, phase, wavelength);
    except ValueError:
        return None;


class lightRay(object):
    """a set of operations you can do to a collection of light Rays"""    

    def __init__ (self, position, pointingToward, n_index = 1, phase = 0, wavelength = 600):
        #%creates a single ray (or many rays)
        #%   position--where it is located [x1 y1 z1] or [[x1,y1,z1],[x2,y2,z2],...]
        #%   pointing toward--will combine with position to make a normalized
        #%   direction vector [[X1,Y1,Z1],[X2,Y2,Z2],...]
        #%   n_index--the index of refraction of the material the light rays are currently in

        position       = np.array(position,float);
        pointingToward = np.array(pointingToward,float);
        n_index        = np.array(n_index,float);

            #case: they passed in a single ray in a one dimensional way
        if len(position.shape) ==1:
            position = np.array([position]);
    
            #case: they passed in a multi-ray array, on its side     
        if position.shape[0] > 4 or pointingToward.shape[0] > 4:  #do both checks, because they can pass in a lot of pointing Toward data OR a lot of position data.
            position = position.T;
            pointingToward = pointingToward.T

        
        #determine the direction based on where you are now, and where you are pointing to.
        direction = pointingToward - position;
   
        if direction.size * position.size == 0:
            raise ValueError; #the sizes are wrong--problem!
            

        """# users don't care that we need a 4th(perspective) dimension to interact with 
        # 2nd order geometric surfaces (spheres etc.), but we also want to allow for
        # the posiblity that this function is called by someone who does know about 
        # the perspective dimension, so we'll just turn both inputs into something useable"""
        zeros = np.zeros(np.max(  (position.shape[1],direction.shape[1])  ));
        self.direction = np.array([zeros,zeros,zeros,zeros])
        # print(self.direction.T);
        self.position  = self.direction.copy();
        self.direction[0:3,:] = direction[0:3,:] + self.direction[0:3,:]
        self.position [0:3,:] = position [0:3,:] + self.position [0:3,:]

        self.direction = unitVector(self.direction)

        #self.direction[3,:] = 0; #this is already implicity happening a few lines up
        self.position[3,:] = 1;

        self.n_index   = zeros + n_index;   #n_index
        self.phase     = zeros + phase;   #phase
        self.wavelength= zeros + wavelength; #wavelength


    def propigate(self, travel_distance):
        """#%returns rays, after they have traveled travel_distance
        #%size(travel_distance) == 1 if all rays travel the same distance
        #%size(travel_distance,2)==size(rays.direction,2) if each ray travels a
        #%       unique distance
        #%note:  this function allows propigation to be negative
        #%note2: travel_distance is in millimeters I believe;
        #global visualize"""
        u = travel_distance * self.direction[0,:];
        v = travel_distance * self.direction[1,:];
        w = travel_distance * self.direction[2,:];
    
        #   this is for when I have time to add plotting functionality
        #    if bitand(visualize,2)
        #        x = rays.position(:,1);
        #        y = rays.position(:,2);
        #        z = rays.position(:,3);
        #        quiver3(x,y,z,u,v,w,0);
        #    end
    
        temp = np.array([u,v,w,u*0]);
        #print(temp.T)
        self.position = self.position + temp; 
        #print(self.position.T);
    
        numWaves = (travel_distance/self.wavelength)*10**6;#wavelength is in nanometers, position is in milimeters.
        newPhase = self.phase + numWaves*self.wavelength;
        #%only want the fractions of wavelengths--whole sin waves repeat
        self.phase = newPhase % self.wavelength;

        return self;

    def hitAndMiss(self, rule):
        
        position   = self.position [:,rule];
        direction  = self.direction[:,rule];
        wavelength = self.wavelength[rule];
        n_index    = self.n_index[rule];
        phase     = self.phase[rule];
        hit = Ray(position , position + direction,n_index,phase,wavelength);

        #flip the rule:
        rule = ~rule;
    
        position   = self.position [:,rule];
        direction  = self.direction[:,rule];
        wavelength = self.wavelength[rule];
        n_index    = self.n_index[rule];
        phase     = self.phase[rule];
        miss = Ray(position , position + direction,n_index,phase,wavelength);
    

        return hit, miss

    def append(self,newRays):
        self.position   = np.append(self.position  , newRays.position ,axis = 1);
        self.direction  = np.append(self.direction , newRays.direction,axis = 1);
        self.wavelength = np.append(self.wavelength, newRays.wavelength);
        self.n_index    = np.append(self.n_index   , newRays.n_index);
        self.phase      = np.append(self.phase     , newRays.phase  );
    
    def clone(self):
        return copy.deepcopy(self);

    def apeture(self, radius = 1, center = [0,0,0]):
        # pick only the rays that are currently less than [radius] away from [center]

        shift2origin = self.position - np.vstack(np.append(center,1));
        dist2 = np.sum(shift2origin*shift2origin, axis = 0);
        hit, miss = self.hitAndMiss( dist2 <= radius*radius);

        return hit, miss

    ########## Rays interacting with Surfaces ############################################

    def get2surf(self, surfMatrix):
        """#function [rays, missRays] = get2surf(rays, surfMatrix)
        #%get2surf(rays, surfMatrix) takes an array of rays, and determines if and when they will intersect the surface described by surfMatrix.
        #%   %a lot of thanks go to
        #%   https://www.cs.uaf.edu/2012/spring/cs481/section/0/lecture/01_26_ray_intersections.html,
        #%   but the simple version is that a ray is defined as a vector [A + tB],
        #%   where A and B are known vectors like [1,2,0] + t*[3,1.5,2]
        #%   and a surface is defined as an equation in xyz, like 3x + y - z = 0.
        #%   We combine the two equations, solve for t, and that is how far the
        #%   vector must travel to reach its destination.
        #    global visualize;"""
        surfD = np.zeros_like(self.direction);
        surfP = surfD.copy();

        #for i in raynge(rays[direction].shape[1]) = 1:size(rays.direction,1)
        surfD = np.dot(surfMatrix, self.direction) ;
        surfP = np.dot(surfMatrix, self.position ) ;
    
        a = np.sum(surfD * self.direction,axis = 0);                                             #a*t^2
        b = np.sum(surfD * self.position ,axis = 0) + np.sum(surfP*self.direction,axis = 0);     #b*t
        c = np.sum(surfP * self.position ,axis = 0);                                             #c*1

        t = np.zeros_like(a);
        
        #   now we are going to solve for what t is for each equation. There are several cases, so we update them as we cover them.
        #   First check if there actually is an a*t^2 component -- if not, our math is easy x = -c/b
        badCase = np.array([np.inf],float); #for if we didn't intersect by the time we traveled to infinity
        up = np.abs(a) < .0001;
        t[up] = -c[up]/b[up];
    
        #now for those weird cases when there wasn't an a or a b-->aka there is no intersection. Mark these cases
        t[up & (np.abs(b) < .001)] = badCase;


        #now for the regular case--we don't need to update the previous sets anymore
        up = ~up;
        
        #for the regular case, use the quadratic formula: x = (-b +- sqrt(b^2-4ac)) / 2a
        # sqrtQuad = sqrt(b^2-4ac)
        sqrtQuad = np.sqrt(b[up]*b[up]-4*a[up]*c[up]);
   
        temp1 = (-b[up] + sqrtQuad)/(2*a[up]);
        temp1[(temp1.imag !=0) + (temp1.real <= 0)] = badCase;
   
        temp2 = (-b[up] - sqrtQuad)/(2*a[up]);
        temp2[(temp2.imag !=0) + (temp2.real <= 0)] = badCase;

        t[up] = np.min([temp1,temp2],axis = 0);

        (hitRays, missRays) = self.hitAndMiss( t != badCase);
        t = t[t!=badCase];

        hitRays = hitRays.propigate(t);
        self = hitRays;
        return self, missRays


    def getGrad(self,surfaceMatrix):
        """#%getGrad takes a surface and a list of rays already touching that surface,
        #%and returns the surface gradient vector at each point the rays are touching.
        #%sM stands for surface Matrix, I just wanted to keep the computations compact
        #%{    
        #  if your matrix coefficients are in a matrix as shown below,
        #        x     y    z    1   
        # x   | _x^2, 0   , 0  , 0 |
        # y   | _xy , _y^2, 0  , 0 |
        # z   | _xz , _yz ,_z^2, 0 |
        # 1   | _x  , _y  ,_z  ,_1 |

        #    Then taking the gradient of your equation returns the coefficients multiplied by:
        #  /            X                        Y                        Z          \    note: surf(i) is column-ordered 
        # |x   | _2x,   ,   ,   |   ,   |    ,   ,   ,   |   ,   |    ,   ,   ,   |  |          |  1  , 5 , 9 , 13 |
        # |y   | _y ,   ,   ,   |   ,   | _x ,_2y,   ,   |   ,   |    ,   ,   ,   |  |          |  2  , 6 ,10 , 14 |
        # |z   | _z ,   ,   ,   |   ,   |    ,_z ,   ,   |   ,   | _x ,_y ,_2z,   |  |          |  3  , 7 ,11 , 15 |
        # |1   | _1 ,   ,   ,   |   ,   |    ,_1 ,   ,   |   ,   |    ,   ,_1 ,   |  |          |  4  , 8 ,12 , 16 |
        #  \                                                                         /

        #For more information, check out
        #    https://www.cs.uaf.edu/2012/spring/cs481/section/0/lecture/01_26_ray_intersections.html
        #%}"""
        gradient = np.dot(surfaceMatrix + surfaceMatrix.T,self.position); #and I think this one works even more efficiently.
        gradient[3,:] = 0;
        return unitVector(gradient);

    def reflect(self, surfMatrix):
        """#%reflect takes vectors hitting a surface, and returns them just after being reflected
        #%   there are two important requirements:
        #%       The rays must have already reached the surface
        #%       their direction vector must be toward the surface."""
        gradVec = self.getGrad(surfMatrix);

        self.direction[0:3,:] = self.direction[0:3,:] - 2* np.sum(self.direction[0:3,:]*gradVec[0:3,:],axis = 0)*gradVec[0:3,:];

        #% mirrors cause a pi phase shift in the wave phase:
        self.phase = (self.phase + self.wavelength/2) % self.wavelength
    
        return self


    def refract(self, surfMatrix, n2 = 1):
        #%refract(rays, surfMatrix, n2)
        #%this function expects unit vectors to come in.
        #%the equation is based on a derivation in the book Introduction to Ray Tracing by glassner
        r = self.n_index/n2; #ratio n1/n2

        #%the 'rule of thumb' for phase reflections caused by refraction is:
        #%n1 to n2:  if high to low?  Phase shift no!
        #%           if low to high?  Phase shift pi!
        phaseShiftPi = self.n_index < n2;
        self.phase[phaseShiftPi] = (self.phase[phaseShiftPi] + self.wavelength[phaseShiftPi]/2) % self.wavelength[phaseShiftPi];
        self.n_index[:] = n2;

        gradVec = self.getGrad(surfMatrix);

        cos1 = np.sum(-self.direction*gradVec,axis = 0);
        gradVec[:,cos1<0] = -gradVec[:,cos1<0];

        cos1 = np.sum(-self.direction*gradVec,axis = 0);
        cos2 = np.lib.scimath.sqrt(1-r*r*(1-cos1*cos1));  #%if imaginary, there was internal reflection;
        toRefl = cos2.imag != 0;
        
        refl = self.direction - 2*cos1*gradVec;
        self.direction = r * ((self.direction - cos1*gradVec) - cos2*gradVec);#refract these rays
        self.direction[:,toRefl] = refl[:,toRefl];#reflect these rays

        self.direction = unitVector(self.direction);
        """#%I believe this is an unnecessary check to ensure that the result is
        #% %normalized; it is guaranteed to be normalized by the equation above.
        #% mag = sqrt(dot(rays.direction(1:3,:),rays.direction(1:3,:),1));
        #% mag(mag == 0) = 1;
        #% rays.direction(1:3,:) = rays.direction(1:3,:)./[mag;mag;mag];
        #% rays.direction(4,:) = 0;"""

        
        reflected, refracted = self.hitAndMiss(toRefl);
    
        return refracted;

def pointSource(center = (0,0,0) , N = 200, r = 1):
    """#This algorithm comes from "How to generate equidistributed points on the surface of a sphere" by Markus Deserno
    #Max-Planck-Institut fur? Polymerforschung, Ackermannweg 10, 55128 Mainz, Germany
    #(Dated: September 28, 2004)
    #http://www.cmu.edu/biolphys/deserno/pdf/sphere_equi.pdf  
    #I need to cite this better
    # N is approximately number of Points you would like to map to the sphere (it might not be exactly N)
    # 'center' is where the sphere will be located
    # sPoint = stored Point"""
    sPoint = np.zeros((N+20,3))
    pi = np.pi
       
    Ncount = 0;                                 #Set Ncount = 0.
    a = 4*pi*r*r/N;                             #Set a = 4?r^2/N 
    d = np.sqrt(a);                             #Set d = sqrt(a)
    M_th = np.round(pi/d)                       #Set Mtheta = round[pi/d].
    d_th = np.pi/M_th                           #Set dtheta = pi/Mtheta
    d_phi = a/d_th                              #Set dphi = a/dtheta.
    for m in range(M_th.astype(int)):           #For each m in 0 . . .Mtheta ? 1 do {
        theta = pi*(m + 0.5)/M_th                   #Set pi\theta = pi(m + 0.5)/Mtheta.
        M_phi = np.round(2*pi*np.sin(theta)/d_phi)  #Set Mphi = round[2pi sin(theta)/dphi]. Possibly should be sin(theta/dphi)
        for n in range(M_phi.astype(int)):          #For each n in 0 . . .M? ? 1 do {
            phi = 2*pi*n/M_phi                           #Set phi = 2pin/Mphi.
            sPoint[Ncount] = [r,theta,phi];              #Store point on surface for later
            Ncount += 1                                  #Ncount += 1.
                                                    #}
                                                    #}
    sPoint = sPoint[0:Ncount];             #chop off preallocated space that wasn't used
                                            
    #We have the points on our unit sphere, in Polar Coordinates.  We want them in Cartesian
    sin_th = np.sin( sPoint[:,1] );             #sin u   |           
    cos_th = np.cos( sPoint[:,1] );             #cos u   |          x     r * sin u * cos u
    sin_phi= np.sin( sPoint[:,2] );             #sin u   |   Note:  y  =  r * sin u * cos u
    cos_phi= np.cos( sPoint[:,2] );             #cos u   |          z     r * cos u

    cartesianSphere = np.array(r*[sin_th*cos_phi,sin_th*sin_phi, cos_th]).T;
    lightSource = Ray(center, center + cartesianSphere);
    return lightSource;


    # and this is from  http://blog.marmakoide.org/?p=1
    #n = 256
 
    #golden_angle = numpy.pi * (3 - numpy.sqrt(5))
    #theta = golden_angle * numpy.arange(n)
    #z = numpy.linspace(1 - 1.0 / n, 1.0 / n - 1, n)
    #radius = numpy.sqrt(1 - z * z)
 
    #points = numpy.zeros((n, 3))
    #points[:,0] = radius * numpy.cos(theta)
    #points[:,1] = radius * numpy.sin(theta)
    #points[:,2] = z
