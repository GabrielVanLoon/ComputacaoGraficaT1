#!/usr/bin/env python3
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders

from src.shaders.Shader import Shader
from src.shaders.BaseShader import vertex_code, fragment_code


class GameObject:
    """
    Abstração básica de um objeto que compõe a cena do jogo (Ex: jogador, obstaculo, fundo).
    Possui  os atributos e métodos comuns a todos. Assume a forma de um quadrado se desenhado
    em tela.

    A criação do programa de Shader e declaração dos vértices é feita apenas uma vez por meio
    de atributos e métodos estáticos (pertencentes à classe).
    """

    shader_program  = Shader(vertex_code, fragment_code)
    shader_offset = 0
    shader_vertices = [ 
        (-1.0,   1.0,  0.0),
        (-1.0,  -1.0,  0.0),
        ( 1.0,   1.0,  0.0),
        ( 1.0,  -1.0,  0.0),
    ]


    def __init__(self, position=(0,0), size=(200,200), rotate=0, window_resolution=(600,600)) -> None:
        """
        Cria um objeto básico com as configurações de posicionamento informadas. a conversão
        da posição em pixels para coordenadas relativas é feita automaticamente.

        Parameters:
        -----------
        position: dupla de inteiros
            Representa a posição em pixels do objeto na janela
        size: dupla de inteiros
            Representa o tamanho (width e height) em pixels do objeto na janela
        rotate: inteiro ou flutuante
            Representa o grau de rotação do objeto
        window_resolution: dupla de inteiros
            Representa o tamanho atual da tela (necessário para realizar algumas conversões)
        """
        self.position = position                   
        self.size = size
        self.rotate = rotate
        self.window_resolution = window_resolution

        self._gl_scale = [0.0, 0.0]
        self._gl_rotate = [0.0]
        self._gl_translate = [0.0, 0.0]

        self.__configure_gl_variables()


    def __configure_gl_variables(self):
        """
        Atualiza as variáveis utilizadas para renderização (__gl_*) baseado nos valores
        das variáveis públicas. 
        
        Ex: posicao (300, 450) -> (0.0, 0.5) em uma tela de 600x600
        """
        self._gl_scale[0] = self.size[0]/self.window_resolution[0]
        self._gl_scale[1] = self.size[1]/self.window_resolution[1]
        self._gl_rotate   = self.rotate*(np.pi/180.0)
        self._gl_translate[0] = (self.position[0] - 0.5*self.window_resolution[0])/ (0.5*self.window_resolution[0])
        self._gl_translate[1] = (self.position[1] - 0.5*self.window_resolution[1])/ (0.5*self.window_resolution[1])


    def _generate_model_matrix(self, scale_first=False) -> list:
        """
        Calcula e retorna a matrix model para realizar as transformações no objeto
        """
        # Translate * Rotate * Scale
        # return [    
        #     self._gl_scale[0]*np.cos(self._gl_rotate), self._gl_scale[1]*-np.sin(self._gl_rotate), 0.0, self._gl_translate[0], 
        #     self._gl_scale[0]*np.sin(self._gl_rotate), self._gl_scale[1]* np.cos(self._gl_rotate), 0.0, self._gl_translate[1], 
        #     0.0, 0.0, 1.0, 0.0, 
        #     0.0, 0.0, 0.0, 1.0
        # ]
        # Translate * Scale * Rotate
        return [    
            self._gl_scale[0]*np.cos(self._gl_rotate), self._gl_scale[0]*-np.sin(self._gl_rotate), 0.0, self._gl_translate[0], 
            self._gl_scale[1]*np.sin(self._gl_rotate), self._gl_scale[1]* np.cos(self._gl_rotate), 0.0, self._gl_translate[1], 
            0.0, 0.0, 1.0, 0.0, 
            0.0, 0.0, 0.0, 1.0
        ]


    def draw(self):
        """
        Assume que o shader do objeto atual já foi ativado e realiza os desenhos na tela. 
        Aplica a matriz model para posicionar o objeto no mundo segundo os parâmetros 
        de posição, rotação e tamanho do objeto.
        """
        # Prepare the model transformation matrix
        model_matrix = np.array(self._generate_model_matrix(), np.float32)

        # Send final matrix to the GPU unit
        GameObject.shader_program.set4fMatrix('u_model_matrix', model_matrix)
        
        # Draw object steps
        glDrawArrays(GL_TRIANGLE_STRIP, GameObject.shader_offset, 4)
