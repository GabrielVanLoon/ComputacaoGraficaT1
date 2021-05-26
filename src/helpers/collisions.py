#!/usr/bin/env python3
import numpy as np


def hitbox_window_collider(position=[0,0], size=[0,0], window_resolution=[600,600]):
    """
    Verifica se um objeto quadrado simples, livre de efeitos de rotação, 
    colidiu com alguma das faces da janela atual.

    Retorna a correção necessária na posição e a direção da 
    força de reação no objeto.
    """
    collision = False
    # reaction_vector = np.array([1.0, 1.0])

    if position[0] + (size[0]/2.0) > window_resolution[0] or position[0] - (size[0]/2.0) < 0:
        collision |= True
        # reaction_vector[0] = -1.0


    if position[1] + (size[1]/2.0) > window_resolution[1] or position[1] - (size[1]/2.0) < 0:
        collision |= True
        # reaction_vector[1] = -1.0

    return collision