#!/usr/bin/env python3
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders
import glfw

from src.shaders.Shader import Shader
from src.shaders.BaseShader import vertex_code, fragment_code
from src.objects.GameObject import GameObject
from src.colliders.Hitbox import Hitbox

class RunningSquareObject(GameObject):
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
    subscribe_keys = [glfw.KEY_A, glfw.KEY_D, glfw.KEY_W, glfw.KEY_S]
    

    def __init__(self, position=(0,0), size=(200,200), rotate=0, window_resolution=(600,600)) -> None:
        super().__init__(position=position, size=size, rotate=rotate, window_resolution=window_resolution)

        self.__delta_translate = 0.1  # Moves 1px each translation iteration


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
        RunningSquareObject.shader_program.set4fMatrix('u_model_matrix', model_matrix)
        
        # Draw object steps
        glDrawArrays(GL_TRIANGLE_STRIP, RunningSquareObject.shader_offset, 4)


    def logic(self, keys={}, buttons={}, objects=[]) -> None:
        """
        Atualiza as posicoes do quadrado com as teclas AWSD 
        """ 

        # Horizontal movement
        collision = False
        last_position = self.position[0]

        self.position[0] -= keys.get(glfw.KEY_A, {"action": 0})["action"] * self.__delta_translate
        self.position[0] += keys.get(glfw.KEY_D, {"action": 0})["action"] * self.__delta_translate
        self.configure_hitbox()
       
        for item in objects: 
            if item != self:
                collision |= self.object_hitbox.check_collision(item.object_hitbox)
            if collision:
                break
        
        if collision:
            self.position[0] = last_position

        # Vertical movement
        collision = False
        last_position = self.position[1]
        
        self.position[1] -= keys.get(glfw.KEY_S, {"action": 0})["action"] * self.__delta_translate
        self.position[1] += keys.get(glfw.KEY_W, {"action": 0})["action"] * self.__delta_translate
        self.configure_hitbox()

        for item in objects: 
            if item != self:
                collision |= self.object_hitbox.check_collision(item.object_hitbox)
            if collision:
                break

        if collision:
            self.position[1] = last_position
            self.configure_hitbox()
        
        self._configure_gl_variables()