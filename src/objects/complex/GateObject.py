#!/usr/bin/env python3
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders
import glfw

from src.shaders.Shader import Shader
from src.shaders.BaseShader import vertex_code, fragment_code
from src.objects.GameObject import GameObject
from src.colliders.Hitbox import Hitbox

class GateObject(GameObject):
    """
    Implementa a forma de um quadrado que se move com as teclas AWSD.
    """

    shader_program  = Shader(vertex_code, fragment_code)
    shader_offset   = 0
    shader_vertices = [ 
        (-0.8 , -0.3 , 0.0), #portao
        (-0.8 , 1.0 , 0.0),
        ( 0.8 , -0.3 , 0.0),
        ( 0.8 , 1.0 , 0.0),

        (-0.8 , 0.8 , 0.0), # risco
        (-0.8 , 0.75 , 0.0),
        ( 0.8 , 0.8 , 0.0),
        ( 0.8 , 0.75 , 0.0),

        (-0.8 , 0.55 , 0.0), # risco
        (-0.8 , 0.5 , 0.0),
        ( 0.8 , 0.55 , 0.0),
        ( 0.8 , 0.5 , 0.0),

        (-0.8 , 0.3 , 0.0), # risco
        (-0.8 , 0.25 , 0.0),
        ( 0.8 , 0.3 , 0.0),
        ( 0.8 , 0.25 , 0.0),

        (-0.8 , 0.0 , 0.0), # risco
        (-0.8 , 0.05 , 0.0),
        ( 0.8 , 0.0 , 0.0),
        ( 0.8 , 0.05 , 0.0),

        (-0.32 , 0.82 , 0.0), # detalhe azul
        (-0.32 , 0.73 , 0.0),
        ( 0.32 , 0.82 , 0.0),
        ( 0.32 , 0.73 , 0.0),

        (-0.32 , 0.58 , 0.0), # detalhe azul
        (-0.32 , 0.47 , 0.0),
        ( 0.32 , 0.58 , 0.0),
        ( 0.32 , 0.47 , 0.0),

        (-0.32 , 0.33 , 0.0), # detalhe azul
        (-0.32 , 0.22 , 0.0),
        ( 0.32 , 0.33 , 0.0),
        ( 0.32 , 0.22 , 0.0),

        (-0.32 , -0.03 , 0.0), # detalhe azul
        (-0.32 , 0.08 , 0.0),
        ( 0.32 , -0.03 , 0.0),
        ( 0.32 , 0.08 , 0.0),
    ]

    subscribe_keys = []
    

    def get_vertices():
        """Geração dos vértices do Portão"""
        return GateObject.shader_vertices


    def __init__(self, position=(0,0), size=(200,200), rotate=0, window_resolution=(600,600)) -> None:
        super().__init__(position=position, size=size, rotate=rotate, window_resolution=window_resolution)


    def configure_hitbox(self) -> None:
        """Define a hitbox"""

        # Check if horizontal or vertical
        if self.rotate == 0:
            box_values = [ self.position[0]-0.8*self.size[0]/2, self.position[1], 
                            self.size[0]*0.8, 0.5*self.size[1] ]
        else:
            box_values = [ self.position[0], self.position[1]-0.8*self.size[1]/2, 
                            0.5*self.size[0], self.size[1]*0.8 ]

        if self.object_hitbox == None:
            self.object_hitbox = Hitbox("box", box_values)
        else: 
            self.object_hitbox.update_values(box_values)


    def draw(self):
        """Desenha o objeto na tela"""
        # Prepare the model transformation matrix
        model_matrix = np.array(self._generate_model_matrix(), np.float32)

        # Send final matrix to the GPU unit
        GateObject.shader_program.set4fMatrix('u_model_matrix', model_matrix)
        
        # Draw object steps
        GateObject.shader_program.set4Float('u_color',[0.69, 0.572, 0.423, 1.0])
        glDrawArrays(GL_TRIANGLE_STRIP, GateObject.shader_offset+0, 4) # portao

        GateObject.shader_program.set4Float('u_color',[0.0, 0.0, 0.0, 1.0])
        glDrawArrays(GL_TRIANGLE_STRIP, GateObject.shader_offset+4, 4) # risco
        glDrawArrays(GL_TRIANGLE_STRIP, GateObject.shader_offset+8, 4) # risco
        glDrawArrays(GL_TRIANGLE_STRIP, GateObject.shader_offset+12, 4) # risco
        glDrawArrays(GL_TRIANGLE_STRIP, GateObject.shader_offset+16, 4) # risco

        GateObject.shader_program.set4Float('u_color',[0.737, 0.925, 0.863, 1.0])
        glDrawArrays(GL_TRIANGLE_STRIP, GateObject.shader_offset+20, 4) # detalhe azul
        glDrawArrays(GL_TRIANGLE_STRIP, GateObject.shader_offset+24, 4) # detalhe azul
        glDrawArrays(GL_TRIANGLE_STRIP, GateObject.shader_offset+28, 4) # detalhe azul
        glDrawArrays(GL_TRIANGLE_STRIP, GateObject.shader_offset+32, 4) # detalhe azul


    def logic(self, keys={}, buttons={}, objects=[]) -> None:
        """
        Portão que realiza downscale no eixo de comprimento quando 
        pressionado e retorna lentamente ao tamanho normal quando não.
        """
        return 
