#!/usr/bin/env python3
import math 
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders
import glfw

from src.shaders.Shader import Shader
from src.shaders.BaseShader import vertex_code, fragment_code
from src.objects.GameObject import GameObject
from src.helpers.vertex import generate_circle_vertexes
from src.helpers.collisions import hitbox_window_collider
from src.colliders.Hitbox import Hitbox

class BoucingBallObject(GameObject):
    """
    Implementa a forma de um quadrado que se move com as teclas AWSD.
    """

    shader_program  = Shader(vertex_code, fragment_code)
    shader_offset   = 0
    shader_vertices = []
    subscribe_keys  = []
    
    def get_vertices():
        """
        Gera dinamicamente os vértices da esfera, salvando os valores 
        calculados no atributo estatico da classe.
        """
        BoucingBallObject.shader_vertices = generate_circle_vertexes(N=32, center=(0,0), radius=1.0)
        return BoucingBallObject.shader_vertices


    def __init__(self, position=(0,0), size=(200,200), rotate=0, window_resolution=(600,600)) -> None:
        super().__init__(position=position, size=size, rotate=rotate, window_resolution=window_resolution)

        self.__delta_translate = 0.05  # Moves 0.1 px each translation iteration
        self.__delta_direction = np.array([1.0, 0.7], dtype=np.float) # Initial direction
        self.__delta_direction = self.__delta_direction / np.linalg.norm(self.__delta_direction)
    

    def configure_hitbox(self) -> None:
        """Define a box type Hitbox"""
        box_values = [ self.position[0]-self.size[0]/2, self.position[1]-self.size[1]/2, 
                        self.size[0], self.size[1] ]

        if self.object_hitbox == None:
            self.object_hitbox = Hitbox("box", box_values)
        else: 
            self.object_hitbox.update_values(box_values)


    def draw(self):
        """
        Desenha o triângulo na tela
        """
        # Prepare the model transformation matrix
        model_matrix = np.array(self._generate_model_matrix(), np.float32)

        # Send final matrix to the GPU unit
        BoucingBallObject.shader_program.set4fMatrix('u_model_matrix', model_matrix)
        
        # Draw object steps
        glDrawArrays(GL_TRIANGLE_FAN, BoucingBallObject.shader_offset, 32)


    def logic(self, keys={}, buttons={}, objects=[]) -> None:
        """
        Atualiza as posicoes do quadrado com as teclas AWSD 
        """ 

        # Horizontal movement
        collision = False
        last_position = self.position[0]

        self.position[0] += self.__delta_translate * self.__delta_direction[0]
        self.configure_hitbox()

        collision |= hitbox_window_collider(self.position, self.size, self.window_resolution)        
        for item in objects: 
            if item != self:
                collision |= self.object_hitbox.check_collision(item.object_hitbox)
            if collision:
                break

        if collision:
            self.position[0] = last_position
            self.__delta_direction[0] *= -1.0

        # Vertical movement
        collision = False
        last_position = self.position[1]

        self.position[1] += self.__delta_translate * self.__delta_direction[1]
        self.configure_hitbox()

        collision |= hitbox_window_collider(self.position, self.size, self.window_resolution)        
        for item in objects: 
            if item != self:
                collision |= self.object_hitbox.check_collision(item.object_hitbox)
            if collision:
                break

        if collision:
            self.position[1] = last_position
            self.__delta_direction[1] *= -1.0

        self._configure_gl_variables()