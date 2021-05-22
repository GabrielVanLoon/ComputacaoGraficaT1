#!/usr/bin/env python3
import glfw
from OpenGL.GL import *


class GameController:
    """
    Classe principal que engloba todos os estados, objetos, controle de janela,
    inputs de usuário e loop principal da lógica do jogo.
    """


    def __init__(self, title="Computer Graphics 101", width=600, height=600, enable3D=False):
        """
        Set the program window configurations and other important variables
        """
        self.__glfw_window = False
        self.__glfw_title  = title
        self.__glfw_width  = width
        self.__glfw_height = height
        self.__glfw_enable3D = enable3D
        self.__configure_window()


    def __configure_window(self):
        """
        Internal function with the GLFW window and context configurations
        """
        glfw.init()
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
        self.__glfw_window = glfw.create_window(self.__glfw_width, self.__glfw_height, self.__glfw_title, None, None)
        glfw.make_context_current(self.__glfw_window)


    def start(self):
        """
        Start the game logic and graphic loop. Runs until the player close the window.
        """
        glfw.show_window(self.__glfw_window)

        if self.__glfw_enable3D:
            glEnable(GL_DEPTH_TEST)

        while not glfw.window_should_close(self.__glfw_window):
            glfw.poll_events() 
            
            # Reset the screen with the white color
            if self.__glfw_enable3D:
                glClear(GL_COLOR_BUFFER_BIT) 
            else:
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
            glClearColor(1.0, 1.0, 1.0, 1.0)
            
            glfw.swap_buffers(self.__glfw_window)
        glfw.terminate()


if __name__ == '__main__':
    game = GameController(title="Testing Game Controller", width=1200, height=600, enable3D=False)
    game.start()