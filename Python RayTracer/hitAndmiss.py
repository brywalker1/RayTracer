import numpy as np

def hitAndMiss(rays, rule):
    hit = {};
    hit['position' ] = rays['position'  ][rule,:];
    hit['direction'] = rays['direction' ][rule,:];
    hit['n_index'  ] = rays['n_index'   ][rule];
    hit['phase'    ] = rays['phase'     ][rule];
    hit['wavelength']= rays['wavelength'][rule];

    #flip the rule:
    rule = ~rule;
    miss = {};
    miss['position' ] = rays['position'  ][rule,:];
    miss['direction'] = rays['direction' ][rule,:];
    miss['n_index'  ] = rays['n_index'   ][rule];
    miss['phase'    ] = rays['phase'     ][rule];
    miss['wavelength']= rays['wavelength'][rule];

    return (hit, miss);