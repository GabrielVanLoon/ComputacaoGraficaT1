#!/usr/bin/env python3
import math
from typing import Collection 
import numpy as np


class Hitbox:
    """
    Implementa técnicas de hitbox mais complexas para iteração entre poligonos 
    sob efeito de rotação, escalonamento e escala.

    Tipos
    -----
    box: [x, y, width, height]
        Hitbox quadrado padrão que define apenas as bordas do objeto.
        Obs: Não deve ser utilizado em objetos que sofrem de rotações.
    polygon: [v_1, v_2, v_3, ..., v_n] 
        Poligono convexo definido pelo conjunto de vertices recebidos
    circle: [x_c, y_c, radius]
        hitbox circular definido pela posicao do centro do circulo e seu raio
    """


    def __init__(self, type="box", args=[]) -> None:
        """
        Inicia o hitbox para ser utilizado pelo objeto. Os valores dos vértices devem
        estar na notação de OpenGL, ou seja, normalizados entre [-1,1] quando visiveis
        dentro da tela.
        """
        self.type = type
        self.box  = []
        self.circle = {}
        self.edges = []
        self.update_values(args)


    def update_values(self, args=[]) -> None:
        """
        Atualiza os valores do hitbox com os valores recebidos
        """
        if self.type == "box":
            self.box = {"x": args[0], "y": args[1], "w": args[2], "h": args[3]}
        elif self.type == "circle":
            self.circle = {"x": args[0], "y": args[1], "r": args[2]}
        else:
            self.edges = args

        
    def check_collision(self, object) -> bool:
        """
        Recebe outro objeto do tipo Hitbox e, dependendo dos tipos
        de hitbox decide pela técnica a ser utilizada.

        Retorna se houve colisão e o vetor de direção da reação do 
        objeto no hitbox atual de forma normalizada.
        """
        
        if self.type == "box" and object.type == "box":
            return self.__box_box_collision(object)

        return False


    def __box_box_collision(self, object) -> bool:
        """Box vs Box collision (AABB method) does not have reaction"""

        collision = True

        collision &= self.box['x'] < object.box['x'] + object.box["w"]
        collision &= self.box['x'] + self.box['w'] > object.box["x"]
        collision &= self.box['y'] < object.box['y'] + object.box["h"]
        collision &= self.box['y'] + self.box['h'] > object.box["y"]

        return collision
            




