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

class RobotObject(GameObject):
    """
    Implementa o Robô que se move constantemente em busca de alcançar
    o objetivo da fase. 
    """

    shader_program  = Shader(vertex_code, fragment_code)
    shader_offset   = 0
    shader_vertices = []
    subscribe_keys  = []

    num_vertices = 10
    
    def get_vertices():
        """Geração dos vértices do Robo"""
        RobotObject.shader_vertices = [
            ( 0.428 , 0.857 , 0.0), # laranja
            ( 1.0 , 0.428 , 0.0),
            ( 0.857 , -0.286 , 0.0),
            ( 0.0 , -0.857 , 0.0),
            ( -0.857 , -0.286 , 0.0),
            ( -1.0 , 0.428 , 0.0),
            ( -0.428 , 0.857 , 0.0),    

            ( 0.428 , 0.857 , 0.0), # preto
            ( 0.642 , 0.714 , 0.0),
            ( 0.286 , 0.214 , 0.0),
            ( -0.286 , 0.214 , 0.0),
            ( -0.642 , 0.714 , 0.0),
            ( -0.428 , 0.857 , 0.0),

            ( 0.643 , 0.714 , 0.0), # azul direita
            ( 1.0 , 0.428 , 0.0),
            ( 0.928 , 0.0 , 0.0),
            ( 0.5 , 0.0 , 0.0),
            ( 0.285 , 0.214 , 0.0),

            ( -0.642 , 0.714 , 0.0), # azul esquerda
            ( -1.0 , 0.428 , 0.0),
            ( -0.928 , 0.0 , 0.0),
            ( -0.5 , 0.0 , 0.0),
            ( -0.285 , 0.214 , 0.0),

            ( 0.285 , 0.214 , 0.0), # contorno smile
            ( 0.5 , 0.0 , 0.0),
            ( 0.214 , -0.571 , 0.0),
            ( -0.214 , -0.571 , 0.0),
            ( -0.5 , 0.0 , 0.0),
            ( -0.285 , 0.214 , 0.0),
        ]

        counter = 29
        radius = 0.0714
        posx = 0.286
        posy = -0.071
        angle = 0.0
        for counter in range(29, 29 + RobotObject.num_vertices):
            angle += 2*math.pi/RobotObject.num_vertices
            x = math.cos(angle)*radius + posx   
            y = math.sin(angle)*radius + posy
            RobotObject.shader_vertices += [(x,y,0.0)]

        counter = 39
        radius = 0.0714
        posx = -0.285
        posy = -0.071
        angle = 0.0
        for counter in range(39, 39 + RobotObject.num_vertices):
            angle += 2*math.pi/RobotObject.num_vertices
            x = math.cos(angle)*radius + posx   
            y = math.sin(angle)*radius + posy
            RobotObject.shader_vertices += [(x,y,0.0)]

        RobotObject.shader_vertices += [
            ( -0.142 , -0.157 , 0.0), # Smiles *W*
            ( -0.128 , -0.142 , 0.0),
            ( -0.043 , -0.257 , 0.0),
            ( -0.036 , -0.236 , 0.0),

            ( -0.043 , -0.257 , 0.0),
            ( -0.057 , -0.242 , 0.0),
            ( 0.0 , -0.2 , 0.0),
            ( 0.0 , -0.185 , 0.0),

            ( 0.043 , -0.257 , 0.0),
            ( 0.057 , -0.242 , 0.0),
            ( 0.0 , -0.2 , 0.0),
            ( 0.0 , -0.185 , 0.0),

            ( 0.143 , -0.157 , 0.0),
            ( 0.128 , -0.142 , 0.0),
            ( 0.043 , -0.257 , 0.0),
            ( 0.036 , -0.236 , 0.0),
        ]

        counter = 65
        radius = 0.857
        posx = -0.786
        posy = 0.0
        angle = math.pi/2
        for counter in range(65, 65 + RobotObject.num_vertices):
            angle += math.pi/RobotObject.num_vertices
            x = math.cos(angle)*radius*0.4 + posx   
            y = math.sin(angle)*radius + posy
            RobotObject.shader_vertices += [(x,y,0.0)]

        counter = 75
        radius = 0.857
        posx = +0.785
        posy = 0.0
        angle = math.pi/2
        for counter in range(75, 75 + RobotObject.num_vertices):
            angle += math.pi/RobotObject.num_vertices
            x = -1*math.cos(angle)*radius*0.4 + posx
            y = math.sin(angle)*radius + posy
            RobotObject.shader_vertices += [(x,y,0.0)]

        return RobotObject.shader_vertices


    def __init__(self, position=(0,0), size=(200,200), rotate=0, window_resolution=(600,600)) -> None:
        super().__init__(position=position, size=size, rotate=rotate, window_resolution=window_resolution)

        self.__delta_translate = 0.2  # Moves 0.1 px each translation iteration
        self.__delta_direction = np.array([0.0, 1.0], dtype=np.float) # Initial direction up
    

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
        RobotObject.shader_program.set4fMatrix('u_model_matrix', model_matrix)
        
        # Draw steps
        RobotObject.shader_program.set4Float('u_color',[0.678, 0.333, 0.118, 1.0])
        glDrawArrays(GL_TRIANGLE_FAN, 0, 7) # perfil

        RobotObject.shader_program.set4Float('u_color',[ 0.153, 0.188, 0.188, 1.0])
        glDrawArrays(GL_TRIANGLE_FAN, 7, 6) # cima

        RobotObject.shader_program.set4Float('u_color',[ 0.290, 0.498, 0.447, 1.0])
        glDrawArrays(GL_TRIANGLE_FAN, 13, 5) # azul direita
        glDrawArrays(GL_TRIANGLE_FAN, 18, 5) # azul esquerda

        RobotObject.shader_program.set4Float('u_color',[ 0.972, 0.898, 0.294, 1.0])
        glDrawArrays(GL_TRIANGLE_FAN, 23, 6) # contorno smile preto

        RobotObject.shader_program.set4Float('u_color',[ 0.647, 0.247, 0.117, 1.0])
        glDrawArrays(GL_TRIANGLE_FAN, 29, RobotObject.num_vertices) #carinha
        glDrawArrays(GL_TRIANGLE_FAN, 29 + RobotObject.num_vertices, RobotObject.num_vertices)
        glDrawArrays(GL_TRIANGLE_STRIP, 29 + 2 * RobotObject.num_vertices, 4)
        glDrawArrays(GL_TRIANGLE_STRIP, 33 + 2 * RobotObject.num_vertices, 4)
        glDrawArrays(GL_TRIANGLE_STRIP, 37 + 2 * RobotObject.num_vertices, 4)
        glDrawArrays(GL_TRIANGLE_STRIP, 41 + 2 * RobotObject.num_vertices, 4)

        RobotObject.shader_program.set4Float('u_color',[ 0.212, 0.231, 0.227, 1.0])
        glDrawArrays(GL_TRIANGLE_FAN, 45 + 2 * RobotObject.num_vertices, RobotObject.num_vertices)
        glDrawArrays(GL_TRIANGLE_FAN, 45 + 3 * RobotObject.num_vertices, RobotObject.num_vertices)


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
                self.position[0] = last_position
                self.__delta_direction[0] *= -1.0
                break
            
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
                self.position[1] = last_position
                self.__delta_direction[1] *= -1.0
                break
            
        self._configure_gl_variables()