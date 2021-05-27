#!/usr/bin/env python3
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders
import glfw

from src.shaders.Shader import Shader
from src.shaders.BaseShader import vertex_code, fragment_code
from src.objects.GameObject import GameObject
from src.colliders.Hitbox import Hitbox

class BoxObject(GameObject):
    """
    Implementa a forma de um quadrado que se move com as teclas AWSD.
    """

    shader_program  = Shader(vertex_code, fragment_code)
    shader_offset   = 0
    shader_vertices = [ 
        ( -1.0 , -1.0 , 0.0), # caixa
        ( 1.0 , -1.0 , 0.0),
        ( -1.0 , 1.0 , 0.0),
        ( 1.0 , 1.0 , 0.0),

        ( -0.9 , -0.7 , 0.0), # caixa contorno interno
        ( -0.9 , 0.9 , 0.0),
        ( 0.9 , -0.7 , 0.0),
        ( 0.9 , 0.9 , 0.0),

        ( -0.9 , 0.8 , 0.0), # caixa diagonal interna
        ( 0.8 , -0.7 , 0.0),
        ( -0.9 , 0.9 , 0.0),
        ( 0.9 , -0.7 , 0.0),
        ( 0.9 , 0.9 , 0.0),

        ( 1.0 , 1.0 , 0.0), # caixa sombra
        ( 1.0 , -1.0 , 0.0),
        ( 1.2 , 1.0 , 0.0),
        ( 1.2 , -1.0 , 0.0),

        ( -0.9 , -0.95 , 0.0), # caixa detalhe
        ( -0.9 , -0.75 , 0.0),
        ( 0.9 , -0.95 , 0.0),
        ( 0.9 , -0.75 , 0.0),
    ]
    subscribe_keys = []

    def get_vertices():
        """Geração dos vértices da Caixa"""
        return BoxObject.shader_vertices


    def __init__(self, position=(0,0), size=(200,200), rotate=0, window_resolution=(600,600)) -> None:
        super().__init__(position=position, size=size, rotate=rotate, window_resolution=window_resolution)


    def configure_hitbox(self) -> None:
        """Define a hitbox"""
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
        BoxObject.shader_program.set4fMatrix('u_model_matrix', model_matrix)
        
        # Draw object steps
        BoxObject.shader_program.set4Float('u_color',[ 0.478, 0.47, 0.419, 1.0])
        glDrawArrays(GL_TRIANGLE_STRIP, BoxObject.shader_offset+0, 4) # perfil

        BoxObject.shader_program.set4Float('u_color',[ 0.556, 0.933, 0.772, 1.0])
        glDrawArrays(GL_TRIANGLE_STRIP, BoxObject.shader_offset+4, 4) # contorno interno

        BoxObject.shader_program.set4Float('u_color',[ 0.427, 0.443, 0.384, 1.0])
        glDrawArrays(GL_TRIANGLE_STRIP, BoxObject.shader_offset+8, 5) # contorno diagonal interna

        # BoxObject.shader_program.set4Float('u_color',[ 0.0, 0.0, 0.0, 0.3])
        # glDrawArrays(GL_TRIANGLE_STRIP, BoxObject.shader_offset+13, 4) # sombra
        
        BoxObject.shader_program.set4Float('u_color',[ 0.427, 0.443, 0.384, 1.0])
        glDrawArrays(GL_TRIANGLE_STRIP, BoxObject.shader_offset+17, 4) # detalhe


    def logic(self, keys={}, buttons={}, objects=[]) -> None:
        """Nenhuma lógica necessária na caixa"""
        return 
