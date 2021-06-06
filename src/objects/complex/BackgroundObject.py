#!/usr/bin/env python3
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders
import glfw

from src.shaders.Shader import Shader
from src.shaders.TextureShader import vertex_code, fragment_code
from src.objects.GameObject import GameObject

class BackgroundObject(GameObject):
    """
    Implementa a forma de um quadrado que se move com as teclas AWSD.
    """

    shader_program  = Shader(vertex_code, fragment_code)
    shader_offset   = 0
    shader_vertices = [ 
                (-1.0,   1.0,  0.0),
        (-1.0,  -1.0,  0.0),
        ( 1.0,   1.0,  0.0),
        ( 1.0,  -1.0,  0.0),
    ]
    shader_textures = ["assets/object_ground_1.jpg"]
    shader_textures_ids = []
    subscribe_keys = []
    

    def get_vertices():
        """Geração dos vértices do Background"""
        return BackgroundObject.shader_vertices


    def __init__(self, position=(0,0), size=(200,200), rotate=0, window_resolution=(600,600)) -> None:
        super().__init__(position=position, size=size, rotate=rotate, window_resolution=window_resolution)


    def draw(self):
        """Desenha o objeto na tela"""
        # Prepare the model transformation matrix
        model_matrix = np.array(self._generate_model_matrix(), np.float32)

        # Send final matrix to the GPU unit
        BackgroundObject.shader_program.set4fMatrix('u_model_matrix', model_matrix)
        BackgroundObject.shader_program.set2Float('u_pattern_repeat', [12,6])
        BackgroundObject.shader_program.setFloat('u_opacity', 0.25)

        # Set Texture id
        glBindTexture(GL_TEXTURE_2D, BackgroundObject.shader_textures_ids[0])

        BackgroundObject.shader_program.set4Float('u_color',[0.93, 0.93, 0.93, 1.0])
        glDrawArrays(GL_TRIANGLE_STRIP, BackgroundObject.shader_offset + 0, 4)