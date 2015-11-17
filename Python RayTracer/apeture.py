import numpy as np
from hitAndmiss import hitAndMiss

def apeture(rays, radius = 1, center = [0,0,0]):

    shift2origin = rays['position'] - center.append(1);

    dist2 = sum(shift2origin*shift2origin, axes = 1);

    hit, miss = hitAndMiss(rays, dist2 <= radius*radius);

    return hit, miss