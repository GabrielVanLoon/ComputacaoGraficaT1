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

class ParedeSageObject(GameObject):
    """
    Implementa a forma de um quadrado que se move com as teclas AWSD.
    """

    shader_program  = Shader(vertex_code, fragment_code)
    shader_offset   = 0
    shader_vertices = [ 
        (-1.0, +1.0, 0.0),
        (-1.0, -1.0, 0.0),
        (-0.5, +1.0, 0.0),
        (-0.5, -1.0, 0.0),

        (-0.5, +1.0, 0.0),
        (-0.5, -1.0, 0.0),
        ( 0.0, +1.0, 0.0),
        ( 0.0, -1.0, 0.0),

        ( 0.0, +1.0, 0.0),
        ( 0.0, -1.0, 0.0),
        (+0.5, +1.0, 0.0),
        (+0.5, -1.0, 0.0),

        (+0.5, +1.0, 0.0),
        (+0.5, -1.0, 0.0),
        (+1.0, +1.0, 0.0),
        (+1.0, -1.0, 0.0),
    ]

    subscribe_keys = []
    

    def get_vertices():
        """Geração dos vértices do Robo"""
        return ParedeSageObject.shader_vertices


    def __init__(self, position=(0,0), size=(200,200), rotate=0, window_resolution=(600,600)) -> None:
        super().__init__(position=position, size=size, rotate=rotate, window_resolution=window_resolution)

        self.__move_direction  = 0 if self.size[0] >= self.size[1] else 1
        self.__delta_translate = 0.1  # Move 1 px each active iteration

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
        ParedeSageObject.shader_program.set4fMatrix('u_model_matrix', model_matrix)
        
        # Draw object steps
        ParedeSageObject.shader_program.set4Float('u_color',[0.729, 0.596, 0.592, 1.0])
        glDrawArrays(GL_TRIANGLE_STRIP, ParedeSageObject.shader_offset + 0, 4) # container

        ParedeSageObject.shader_program.set4Float('u_color',[0.314, 0.659, 0.482, 1.0])
        glDrawArrays(GL_TRIANGLE_STRIP, ParedeSageObject.shader_offset + 0, 4) # esquerda
        glDrawArrays(GL_TRIANGLE_STRIP, ParedeSageObject.shader_offset + 4, 4) # esquerda centro
        glDrawArrays(GL_TRIANGLE_STRIP, ParedeSageObject.shader_offset + 8, 4) # direita centro
        glDrawArrays(GL_TRIANGLE_STRIP, ParedeSageObject.shader_offset + 12, 4) # direita


    def logic(self, keys={}, buttons={}, objects=[]) -> None:
        """
        Parede se move em seu eixo de maio comprimento, precisando verificar
        também se não vai sobrepor nenhum outro objeto
        """

        # Salvando estado anterior
        collision = False
        last_position = self.position[self.__move_direction]
        
        # Realiza o movimento 
        self.position[self.__move_direction] += buttons.get(glfw.MOUSE_BUTTON_LEFT, {"action": 0})["action"] * self.__delta_translate
        self.position[self.__move_direction] -= buttons.get(glfw.MOUSE_BUTTON_RIGHT, {"action": 0})["action"] * self.__delta_translate
        self.configure_hitbox()

        # Verificando se o movimento é válido
        collision |= hitbox_window_collider(self.position, self.size, self.window_resolution)
        for item in objects: 
            if collision:
                break
            if item != self:
                collision |= self.object_hitbox.check_collision(item.object_hitbox)
        
        # Se colidiu cancela o movimento e retorna estado anterior
        if collision:
            self.position[self.__move_direction] = last_position
            self.configure_hitbox()

        self._configure_gl_variables()
        
