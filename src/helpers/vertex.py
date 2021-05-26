#!/usr/bin/env python3
import numpy as np

def generate_circle_vertexes(N=64, center=(0,0), radius=1.0) -> list:
    """
    Dado uma quantidade de vértices, a posição do centro e o raio, gera
    os vértices (notação openGL [-1,1]) que geram a forma de um círculo.
    """

    circle_points = []
    for i in range(0, N): 
        x = center[0] + radius * np.cos(2*i*np.pi/N)
        y = center[1] + radius * np.sin(2*i*np.pi/N)
        circle_points += [(x, y, 0.0)]
    return circle_points