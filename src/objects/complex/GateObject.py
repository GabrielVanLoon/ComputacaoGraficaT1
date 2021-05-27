#!/usr/bin/env python3
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders
import glfw

from src.shaders.Shader import Shader
from src.shaders.BaseShader import vertex_code, fragment_code
from src.objects.GameObject import GameObject
from src.colliders.Hitbox import Hitbox
from src.helpers.collisions import hitbox_window_collider

class GateObject(GameObject):
    """
    Implementa a forma de um quadrado que se move com as teclas AWSD.
    """

    shader_program  = Shader(vertex_code, fragment_code)
    shader_offset   = 0
    shader_vertices = [ 
        (-1.0 , -1.1 , 0.0), #portao
        (-1.0 ,  1.0 , 0.0),
        ( 1.0 , -1.1 , 0.0),
        ( 1.0 ,  1.0 , 0.0),

        (-1.0 , 0.6 , 0.0), # risco
        (-1.0 , 0.5 , 0.0),
        ( 1.0 , 0.6 , 0.0),
        ( 1.0 , 0.5 , 0.0),

        (-1.0 , 0.1 , 0.0), # risco
        (-1.0 , 0.0 , 0.0),
        ( 1.0 , 0.1 , 0.0),
        ( 1.0 , 0.0 , 0.0),

        (-1.0 , -0.4 , 0.0), # risco
        (-1.0 , -0.5 , 0.0),
        ( 1.0 , -0.4 , 0.0),
        ( 1.0 , -0.5 , 0.0),

        (-1.0 , -1.0 , 0.0), # risco
        (-1.0 , -0.9 , 0.0),
        ( 1.0 , -1.0 , 0.0),
        ( 1.0 , -0.9 , 0.0),

        (-0.4 , 0.64 , 0.0), # detalhe azul
        (-0.4 , 0.46 , 0.0),
        ( 0.4 , 0.64 , 0.0),
        ( 0.4 , 0.46 , 0.0),

        (-0.4 , 0.16 , 0.0), # detalhe azul
        (-0.4 ,-0.06 , 0.0),
        ( 0.4 , 0.16 , 0.0),
        ( 0.4 ,-0.06 , 0.0),

        (-0.4 ,-0.34 , 0.0), # detalhe azul
        (-0.4 ,-0.56 , 0.0),
        ( 0.4 ,-0.34 , 0.0),
        ( 0.4 ,-0.56 , 0.0),

        (-0.4 ,-1.06 , 0.0), # detalhe azul
        (-0.4 ,-0.84 , 0.0),
        ( 0.4 ,-1.06 , 0.0),
        ( 0.4 ,-0.84 , 0.0),
    ]

    subscribe_keys = []
    

    def get_vertices():
        """Geração dos vértices do Portão"""
        return GateObject.shader_vertices


    def __init__(self, position=(0,0), size=(200,200), rotate=0, window_resolution=(600,600)) -> None:
        super().__init__(position=position, size=size, rotate=rotate, window_resolution=window_resolution)

        self.__move_direction  = 0 if self.size[0] >= self.size[1] else 1
        self.__delta_shrink = 0.1  # diminui/aumenta 0.1 px por iteração
        self.__original_size = np.array([size[0], size[1]], dtype=np.float)
        self.__original_position = np.array([position[0], position[1]], dtype=np.float)


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
        Portão que se alonga ou estica no eixo de maior comprimento. 
        Porém mantém um ponto fixo de referência no topo/direita.
        """

        # Salvando estado anterior
        collision = False
        last_position = self.position[self.__move_direction]
        last_size     = self.size[self.__move_direction]
        
        # Realiza o movimento 
        reference = self.__original_position[self.__move_direction] - self.__original_size[self.__move_direction]/2.0

        self.size[self.__move_direction] += buttons.get(glfw.MOUSE_BUTTON_LEFT, {"action": 0})["action"] * self.__delta_shrink
        self.size[self.__move_direction] -= buttons.get(glfw.MOUSE_BUTTON_RIGHT, {"action": 0})["action"] * self.__delta_shrink
        
        # Impede ser menor que 10% ou maior que o original
        if self.size[self.__move_direction] < 0.1*self.__original_size[self.__move_direction]:
            self.size[self.__move_direction] = 0.1*self.__original_size[self.__move_direction]
        elif self.size[self.__move_direction] > self.__original_size[self.__move_direction]:
            self.size[self.__move_direction]  = self.__original_size[self.__move_direction]

        # Atualiza a posição
        self.position[self.__move_direction] = (reference + self.size[self.__move_direction])/2.0
        self.configure_hitbox()

        # Verificando se o movimento é válido
        # collision |= hitbox_window_collider(self.position, self.size, self.window_resolution)
        for item in objects: 
            if collision:
                break
            if item != self:
                collision |= self.object_hitbox.check_collision(item.object_hitbox)
        
        # Se colidiu cancela o movimento e retorna estado anterior
        if collision:
            self.position[self.__move_direction] = last_position
            self.size[self.__move_direction] = last_size
            self.configure_hitbox()

        self._configure_gl_variables()
        
