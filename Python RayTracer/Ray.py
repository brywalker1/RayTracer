import collections
import numpy as np
def Ray(position, pointingToward, n_index = 1):
    #%creates a single ray (or many rays)
    #%   position--where it is located [x1 y1 z1]
    #%   pointing toward--will combine with position to make a normalized
    #%   direction vector
    #%   n_index

    position       = np.array(position,float);
    pointingToward = np.array(pointingToward,float);
    n_index        = np.array(n_index,float);

        #case: they passed in a single ray in a one dimensional way
    if len(position.shape) ==1:
        position = np.array([position]);
    
        #case: they passed in a multi-ray array, on its side     
    elif position.shape[1] > 4:
        position = position.T;
        pointingToward = pointingToward.T

    #determine the direction based on where you are now, and where you are pointing to.
    direction = pointingToward - position;
   
    # users don't care that we need a 4th(perspective) dimension to interact with 
    # 2nd order geometric surfaces (spheres etc.), but we also want to allow for
    # the posiblity that this function is called by someone who does know about 
    # the perspective dimension, so we'll just turn both inputs into something useable
    zeros = np.zeros(np.max(  (len(position),len(direction))  ));
    direction4D = np.array([zeros,zeros,zeros,zeros]).T
    position4D  = direction4D.copy();
    direction4D[:,0:3] = direction[:,0:3] + direction4D[:,0:3]
    position4D [:,0:3] = position [:,0:3] + position4D [:,0:3]

    mag = np.array( [np.sqrt(np.sum( direction4D*direction4D ,axis = 1))] ).T;
    mag[mag==0] = 1; #mag(mag==0) = 1;
    direction4D = direction4D/mag; #get unit vectors for our directions

    #direction4D[:,3] = 0; #this is already implicity happening a few lines up
    position4D[:,3] = 1;

    n_index   = np.zeros_like(mag) + n_index;   #n_index
    wavephase = np.zeros_like(mag) + 0;   #phase
    wavelength= np.zeros_like(mag) + 600; #wavelength

    # put the data in columns
    n_index   = np.vstack(n_index);
    wavephase = np.vstack(wavephase);
    wavelength= np.vstack(wavelength);

    ray = {'position':position4D,'direction':direction4D,'n_index':n_index,'phase':wavephase,'wavelength':wavelength };
    return ray;
   