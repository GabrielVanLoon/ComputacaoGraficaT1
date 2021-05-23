#!/usr/bin/env python3
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders

from src.shaders.Shader import Shader
from src.shaders.BaseShader import vertex_code, fragment_code
from src.objects.GameObject import GameObject

class TriangleObject(GameObject):
    """
    Implementa a forma de um triângulo na tela.
    """

    shader_program  = Shader(vertex_code, fragment_code)
    shader_offset = 0
    shader_vertices = [ 
        (-1.0,  -1.0,  0.0),
        ( 0.0,   1.0,  0.0),
        ( 1.0,  -1.0,  0.0),
    ]

    def __init__(self, position=(0,0), size=(200,200), rotate=0, window_resolution=(600,600)) -> None:
        super().__init__(position=position, size=size, rotate=rotate, window_resolution=window_resolution)

    def draw(self):
        """
        Desenha o triângulo na tela
        """
        # Prepare the model transformation matrix
        model_matrix = np.array(self._generate_model_matrix(), np.float32)

        # Send final matrix to the GPU unit
        TriangleObject.shader_program.set4fMatrix('u_model_matrix', model_matrix)
        
        # Draw object steps
        glDrawArrays(GL_TRIANGLES, TriangleObject.shader_offset, 3)