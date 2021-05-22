#!/usr/bin/env python3
from OpenGL.GL import *
import OpenGL.GL.shaders


class Shader:
    """
    Classe que encapsula todo o processo de leitura, compilação e linkagem dos 
    shaders de vértices e fragmentos, além de possuir as diretivas básicas para 
    manipulação dos uniforms
    """


    def __init__(self, vertex_code = "", fragment_code = ""):
        """
        Build a shader program with the vertex and fragment code received. It also
        save previously all the uniforms locations used in the shader. 
        
        Obs: The vertex shader must have the `attribute vec3 position;`.
        """
        # Starting the attributes
        self.__program  = glCreateProgram()
        self.__uniforms = {}
        self.__attributes = {}

        # Create the vertex and shader program
        vertex   = glCreateShader(GL_VERTEX_SHADER)
        fragment = glCreateShader(GL_FRAGMENT_SHADER)

        # Set shaders sources code
        glShaderSource(vertex, vertex_code)
        glShaderSource(fragment, fragment_code)

        # Compiling vertex shader
        glCompileShader(vertex)
        if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(vertex).decode()
            print(error)
            raise RuntimeError("Erro de compilacao do Vertex Shader")

        # Compile fragment shader
        glCompileShader(fragment)
        if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(fragment).decode()
            print(error)
            raise RuntimeError("Erro de compilacao do Fragment Shader")

        # If success atach the compiled codes to the program
        glAttachShader(self.__program, vertex)
        glAttachShader(self.__program, fragment)

        # Build program
        glLinkProgram(self.__program)
        if not glGetProgramiv(self.__program, GL_LINK_STATUS):
            print(glGetProgramInfoLog(self.__program))
            raise RuntimeError('Linking error')

        # Delete shaders (we don't need them anymore after compile)
        glDeleteShader(vertex)
        glDeleteShader(fragment)

        # Save the position attrib location
        self.__attributes['position'] = glGetAttribLocation(self.__program, "position")


    def use(self):
        """Activate the current shader program to be used in GPU."""
        glUseProgram(self.__program)
        glEnableVertexAttribArray(self.__attributes['position'])
        glVertexAttribPointer(self.__attributes['position'], 3, GL_FLOAT, False, 12, ctypes.c_void_p(0))


    def setFloat(self, name, value):
        """Uniform Helper"""
        if not self.__uniforms[name]:
            self.__uniforms[name] = glGetUniformLocation(self.__program, name)
        glUniform1f(self.__uniforms[name], value)


    def set3Float(self, name, value):
        """Uniform Helper"""
        if not self.__uniforms[name]:
            self.__uniforms[name] = glGetUniformLocation(self.__program, name)
        glUniform3f(self.__uniforms[name], value[0], value[1], value[2])