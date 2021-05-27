#!/usr/bin/env python3
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders
import glfw

from src.shaders.Shader import Shader
from src.shaders.BaseShader import vertex_code, fragment_code
from src.objects.GameObject import GameObject
from src.colliders.Hitbox import Hitbox
from src.helpers.vertex import generate_circle_vertexes

class RotatorObject(GameObject):
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
    subscribe_keys = []
    

    def get_vertices():
        """Geração dos vértices do Robo"""
        RotatorObject.shader_vertices += generate_circle_vertexes(32, radius=0.7)
        return RotatorObject.shader_vertices


    def __init__(self, position=(0,0), size=(200,200), rotate=0, window_resolution=(600,600)) -> None:
        super().__init__(position=position, size=size, rotate=rotate, window_resolution=window_resolution)


    def configure_hitbox(self) -> None:
        """Define a hitbox"""
        box_values = [ self.position[0]-0.7*self.size[0]/2, self.position[1]-0.7*self.size[1]/2, 
                        0.7*self.size[0], 0.7*self.size[1] ]

        if self.object_hitbox == None:
            self.object_hitbox = Hitbox("box", box_values)
        else: 
            self.object_hitbox.update_values(box_values)


    def draw(self):
        """Desenha o objeto na tela"""
        # Prepare the model transformation matrix
        model_matrix = np.array(self._generate_model_matrix(), np.float32)

        # Send final matrix to the GPU unit
        RotatorObject.shader_program.set4fMatrix('u_model_matrix', model_matrix)
        
        # Draw object steps
        glDrawArrays(GL_TRIANGLE_STRIP, RotatorObject.shader_offset, 4)

        # Draw Internal Circle
        RotatorObject.shader_program.set4Float('u_color',[1.0,0,0,1.0])
        glDrawArrays(GL_TRIANGLE_FAN, RotatorObject.shader_offset + 4, 32)
        RotatorObject.shader_program.set4Float('u_color',[0.0,0,0,1.0])


    def logic(self, keys={}, buttons={}, objects=[]) -> None:
        """Rotaciona o circulo interno caso ativado"""
        return 
