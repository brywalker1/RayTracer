import numpy as np
from rayTracer import Ray

def initScreens(LEDradius = 80, ViewingRadius = 25, numPoints = 51):

    x  = np.linspace(-LEDradius-20,LEDradius+20,numPoints)
    dist = (x[1]-x[0])/2;
    x2 = x + dist
    y = x*np.sqrt(3)/2; #this preps us for a hexagonal grid.
    z = -2;  #don't want to forget to tell it where the LED's are emitting from
    zeros = np.zeros_like(x);
    positions = np.array([]);

    for row in range(x.shape[0]):
        if (row+1) %2:
            ps = np.array([x,zeros+y[row],zeros]).T;
        else:
            ps = np.array([x2,zeros+y[row],zeros]).T;
        ##find the ones we want
        #ps = np.array([x,zeros + x[row], zeros]).T;
        if positions.size == 0:
            positions = ps;
        else:
            positions = np.append(positions,ps,axis = 0);

    LEDscreen = positions[np.sum(positions*positions,axis = 1) <= LEDradius*LEDradius]
    ViewScreen= positions[np.sum(positions*positions,axis = 1) <= ViewingRadius*ViewingRadius]
    LEDscreen = LEDscreen + np.array([0,0,z]);

    direction =  [0,0,-1];#np.random.randint(-5000,5000,3) + [0,0,-5000];

    LEDrays = Ray(LEDscreen,LEDscreen+direction);
    _, LEDrays = LEDrays.apeture(ViewingRadius,[0,0,z]);#we want everything but a hole in the middle.
    return (LEDrays, ViewScreen, dist);