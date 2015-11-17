import numpy as np
from Ray import Ray
def pointSource( center = (0,0,0) , N = 200):
    #This algorithm comes from "How to generate equidistributed points on the surface of a sphere" by Markus Deserno
    #Max-Planck-Institut fur� Polymerforschung, Ackermannweg 10, 55128 Mainz, Germany
    #(Dated: September 28, 2004)
    #http://www.cmu.edu/biolphys/deserno/pdf/sphere_equi.pdf  
    #I need to cite this better
    # N is approximately number of Points you would like to map to the sphere (it might not be exactly N)
    # 'center' is where the sphere will be located
    # sPoint = stored Point
    sPoint = np.zeros((N+20,3))
    pi = np.pi
    r = 1 
       
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

    return Ray(center, center + cartesianSphere);


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