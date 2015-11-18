import numpy as np
from rayTracer import Ray

def score(rays, apeturePoints, viewingAngles, apetureRadius):

    overall_score = 0.;
    numNans = 0;
    for i in range(len(apeturePoints)):
        subRays,_ = rays.apeture(apetureRadius, apeturePoints[i]);
        if subRays is None:
            subscore = -10;
        else:
            maxes = np.max(np.dot(subRays.direction.T, viewingAngles ),axis = 0);#axis = 1 gives us the best angle for a ray, axis 0 gives us the best ray for the angle
            subscore = np.sum(maxes);

        if np.isnan(subscore):
            numNans += 1;
        else:
            overall_score += subscore;

    return overall_score

"""import numpy as np
from apeture import apeture
def score(rays, apeturePoints, viewingAngles, apetureRadius):

    radius = 3;
    score = 0;
    for i in range(len(apeturePoints)):
        subRays = apeture(rays, apetureRadius, apeturePoints[i]);
        score += np.sum(np.max(np.dot(viewingAngles, subRays),axis = 1));

    return score
    """
