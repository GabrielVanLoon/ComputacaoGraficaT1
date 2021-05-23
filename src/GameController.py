#!/usr/bin/env python3
import glfw
import numpy as np
from OpenGL.GL import *


from src.objects.GameObject import GameObject
from src.objects.geometrics.TriangleObject import TriangleObject


class GameController:
    """
    Classe principal que engloba todos os estados, objetos, controle de janela,
    inputs de usuário e loop principal da lógica do jogo.
    """


    def __init__(self, title="Computer Graphics 101", width=600, height=600, enable3D=False) -> None:
        """
        Set the program window configurations and other important variables
        """
        self.__glfw_window = False
        self.__glfw_title  = title
        self.__glfw_resolution  = (width, height)
        self.__glfw_enable3D = enable3D
        self.__configure_window()
        
        self.__objects = []
        self.__vertices = []
        self.__buffer = None

        self.__configure_objects()
        self.__configure_buffer()


    def __configure_window(self) -> None:
        """
        Internal function with the GLFW window and context configurations
        """
        glfw.init()
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
        self.__glfw_window = glfw.create_window(self.__glfw_resolution[0], self.__glfw_resolution[1], self.__glfw_title, None, None)
        glfw.make_context_current(self.__glfw_window)

        # Compile shaders after create context
        GameObject.shader_program.compile()
        TriangleObject.shader_program.compile()


    def __configure_objects(self) -> None:
        """
        Start/Restart all objects used in the game
        """
        self.__objects  += [ GameObject(position=(300,300), size=(400,200), rotate=45,  window_resolution=self.__glfw_resolution) ]
        GameObject.shader_offset = len(self.__vertices)
        self.__vertices += GameObject.shader_vertices

        self.__objects  += [ TriangleObject(position=(700,300), window_resolution=self.__glfw_resolution) ]
        TriangleObject.shader_offset = len(self.__vertices)
        self.__vertices += TriangleObject.shader_vertices


    def __configure_buffer(self) -> None:
        """
        Instantiate a buffer in GPU and send the vertex data.
        """
        self.__vertices = np.array(self.__vertices, dtype=np.float32)
        self.__buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.__buffer)
        glBufferData(GL_ARRAY_BUFFER, self.__vertices.nbytes, self.__vertices, GL_STATIC_DRAW)



    def start(self) -> None:
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
            
            # Draw objects in the screen
            GameObject.shader_program.use()
            for object in self.__objects:
                object.draw()

            glfw.swap_buffers(self.__glfw_window)
        glfw.terminate()


if __name__ == '__main__':
    game = GameController(title="Testing Game Controller", width=1200, height=600, enable3D=False)
    game.start()