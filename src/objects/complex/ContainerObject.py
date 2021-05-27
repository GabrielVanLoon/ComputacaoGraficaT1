#!/usr/bin/env python3
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders
import glfw

from src.shaders.Shader import Shader
from src.shaders.BaseShader import vertex_code, fragment_code
from src.objects.GameObject import GameObject
from src.colliders.Hitbox import Hitbox

class ContainerObject(GameObject):
    """
    Implementa a forma de um quadrado que se move com as teclas AWSD.
    """

    shader_program  = Shader(vertex_code, fragment_code)
    shader_offset   = 0
    shader_vertices = [
        (-1.0, +1.0, 0.0),
        (-1.0, -1.0, 0.0),
        (+1.0, +1.0, 0.0),
        (+1.0, -1.0, 0.0),

        (-0.75,  +0.9, 0.0),
        (-0.75,  -0.9, 0.0),
        (-0.625, +0.9, 0.0),
        (-0.625, -0.9, 0.0),

        (-0.375, -0.9, 0.0),
        (-0.25,  -0.9, 0.0),
        (-0.625,  0.0, 0.0),
        (-0.5,    0.0, 0.0),
        (-0.375, +0.9, 0.0),
        (-0.25,  +0.9, 0.0),

        (-0.125, +0.9, 0.0),
        ( 0.0,   +0.9, 0.0),
        (-0.125, -0.9, 0.0),
        ( 0.0,   -0.9, 0.0),

        ( 0.0,   +0.9, 0.0),
        ( 0.0,   +0.0, 0.0),
        (+0.125, -0.0, 0.0),
        (+0.125, -0.9, 0.0),

        (+0.125, -0.9, 0.0),
        (+0.25,  -0.9, 0.0),
        (+0.125, +0.9, 0.0),
        (+0.25,  +0.9, 0.0),

        (+0.875, +0.9, 0.0),
        (+0.375, +0.9, 0.0),
        (+0.875, +0.5, 0.0),
        (+0.375, +0.5, 0.0),

        (+0.375, +0.9, 0.0),
        (+0.5,   +0.9, 0.0),
        (+0.375, -0.9, 0.0),
        (+0.5,   -0.9, 0.0),

        (+0.375, -0.9, 0.0),
        (+0.375, -0.5, 0.0),
        (+0.875, -0.9, 0.0),
        (+0.875, -0.5, 0.0),

        (+0.875, -0.9, 0.0),
        (+0.75,  -0.9, 0.0),
        (+0.875, +0.15, 0.0),
        (+0.75,  +0.15, 0.0),

        (+0.875, +0.15, 0.0),
        (+0.875, -0.25, 0.0),
        (+0.625, +0.15, 0.0),
        (+0.625, -0.25, 0.0)
    ]
    subscribe_keys = []
    

    def get_vertices():
        """Geração dos vértices do Robo"""
        return ContainerObject.shader_vertices


    def __init__(self, position=(0,0), size=(200,200), rotate=0, window_resolution=(600,600)) -> None:
        super().__init__(position=position, size=size, rotate=rotate, window_resolution=window_resolution)


    def configure_hitbox(self) -> None:
        """Define a hitbox"""

        # Check if horizontal or vertical
        box_values = [ self.position[0]-self.size[0]/2, self.position[1]-self.size[1]/2, 
                self.size[0], self.size[1] ]
      
        if self.object_hitbox == None:
            self.object_hitbox = Hitbox("box", box_values)
        else: 
            self.object_hitbox.update_values(box_values)


    def draw(self):
        """Desenha o objeto na tela"""
        # Prepare the model transformation matrix
        model_matrix = np.array(self._generate_model_matrix(), np.float32)

        # Send final matrix to the GPU unit
        ContainerObject.shader_program.set4fMatrix('u_model_matrix', model_matrix)
        
        # Draw object steps
        ContainerObject.shader_program.set4Float('u_color',[0.729, 0.596, 0.592, 1.0])
        glDrawArrays(GL_TRIANGLE_STRIP, ContainerObject.shader_offset + 0, 4) # container

        ContainerObject.shader_program.set4Float('u_color',[0.882, 0.835, 0.921, 1.0])
        glDrawArrays(GL_TRIANGLE_STRIP, ContainerObject.shader_offset + 4, 4) # K
        glDrawArrays(GL_TRIANGLE_STRIP, ContainerObject.shader_offset + 8, 6) # K
        glDrawArrays(GL_TRIANGLE_STRIP, ContainerObject.shader_offset + 14, 4) # N
        glDrawArrays(GL_TRIANGLE_STRIP, ContainerObject.shader_offset + 18, 4) # N
        glDrawArrays(GL_TRIANGLE_STRIP, ContainerObject.shader_offset + 22, 4) # N
        glDrawArrays(GL_TRIANGLE_STRIP, ContainerObject.shader_offset + 26, 4) # G
        glDrawArrays(GL_TRIANGLE_STRIP, ContainerObject.shader_offset + 30, 4) # G
        glDrawArrays(GL_TRIANGLE_STRIP, ContainerObject.shader_offset + 34, 4) # G
        glDrawArrays(GL_TRIANGLE_STRIP, ContainerObject.shader_offset + 38, 4) # G
        glDrawArrays(GL_TRIANGLE_STRIP, ContainerObject.shader_offset + 42, 4) # G


    def logic(self, keys={}, buttons={}, objects=[]) -> None:
        """Nenhuma lógica necessária no container"""
        return 
