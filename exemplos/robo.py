import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math as math

glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
window = glfw.create_window(720, 600, "transformation", None, None)
glfw.make_context_current(window)

vertex_code = """
        attribute vec2 position;
        uniform mat4 mat_transformation;
        void main(){
            gl_Position = mat_transformation * vec4(position,0.0,1.0);
        }
        """

fragment_code = """
        uniform vec4 color;
        void main(){
            gl_FragColor = color;
        }
        """

# Request a program and shader slots from GPU
program  = glCreateProgram()
vertex   = glCreateShader(GL_VERTEX_SHADER)
fragment = glCreateShader(GL_FRAGMENT_SHADER)

# Set shaders source
glShaderSource(vertex, vertex_code)
glShaderSource(fragment, fragment_code)

# Compile shaders
glCompileShader(vertex)
if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(vertex).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Vertex Shader")

glCompileShader(fragment)
if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(fragment).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Fragment Shader")

# Attach shader objects to the program
glAttachShader(program, vertex)
glAttachShader(program, fragment)

# Build program
glLinkProgram(program)
if not glGetProgramiv(program, GL_LINK_STATUS):
    print(glGetProgramInfoLog(program))
    raise RuntimeError('Linking error')
    
# Make program the default program
glUseProgram(program)

num_vertices = 10 # define a "qualidade" do circulo

# preparando espaço para 3 vértices usando 2 coordenadas (x,y)
vertices = np.zeros((45 + 4 * num_vertices), [("position", np.float32, 2)])

# preenchendo as coordenadas de cada vértice
vertices[0] = [+0.428, +0.857]  #laranja
vertices[1] = [+1.0, +0.428]
vertices[2] = [+0.857, -0.286]
vertices[3] = [ 0.0, -0.857]
vertices[4] = [-0.857, -0.286]
vertices[5] = [-1.0, +0.428]
vertices[6] = [-0.428, +0.857]

vertices[7] = [+0.428, +0.857]  #preto
vertices[8] = [+0.642, +0.714]
vertices[9] = [+0.286, +0.214]
vertices[10] = [-0.286, +0.214]
vertices[11] = [-0.642, +0.714]
vertices[12] = [-0.428, +0.857]

vertices[13] = [+0.643, +0.714] #azul direita
vertices[14] = [+1.0, +0.428]
vertices[15] = [+0.928,  0.0]
vertices[16] = [+0.5,  0.0]
vertices[17] = [+0.285, +0.214]

vertices[18] = [-0.642, +0.714] #azul esquerda
vertices[19] = [-1.0, +0.428]
vertices[20] = [-0.928,  0.0]
vertices[21] = [-0.5,  0.0]
vertices[22] = [-0.285, +0.214]

vertices[23] = [+0.285, +0.214] #contorno smile preto
vertices[24] = [+0.5,  0.0]
vertices[25] = [+0.214, -0.571]
vertices[26] = [-0.214, -0.571]
vertices[27] = [-0.5,  0.0]
vertices[28] = [-0.285, +0.214]

counter = 29
radius = 0.0714
posx = 0.286
posy = -0.071
angle = 0.0
for counter in range(29, 29 + num_vertices):
    angle += 2*math.pi/num_vertices
    x = math.cos(angle)*radius + posx   
    y = math.sin(angle)*radius + posy
    vertices[counter] = [x,y]

counter = 39
radius = 0.0714
posx = -0.285
posy = -0.071
angle = 0.0
for counter in range(39, 39 + num_vertices):
    angle += 2*math.pi/num_vertices
    x = math.cos(angle)*radius + posx   
    y = math.sin(angle)*radius + posy
    vertices[counter] = [x,y]

vertices[49] = [-0.142, -0.157]
vertices[50] = [-0.128, -0.142]
vertices[51] = [-0.043, -0.257]
vertices[52] = [-0.036, -0.236]

vertices[53] = [-0.043, -0.257]
vertices[54] = [-0.057, -0.242]
vertices[55] = [ 0.0, -0.2]
vertices[56] = [ 0.0, -0.185]

vertices[57] = [+0.043, -0.257]
vertices[58] = [+0.057, -0.242]
vertices[59] = [ 0.0, -0.2]
vertices[60] = [ 0.0, -0.185]

vertices[61] = [+0.143, -0.157]
vertices[62] = [+0.128, -0.142]
vertices[63] = [+0.043, -0.257]
vertices[64] = [+0.036, -0.236]

counter = 65
radius = 0.857
posx = -0.786
posy = 0.0
angle = math.pi/2
for counter in range(65, 65 + num_vertices):
    angle += math.pi/num_vertices
    x = math.cos(angle)*radius*0.4 + posx   
    y = math.sin(angle)*radius + posy
    vertices[counter] = [x,y]

counter = 75
radius = 0.857
posx = +0.785
posy = 0.0
angle = math.pi/2
for counter in range(75, 75 + num_vertices):
    angle += math.pi/num_vertices
    x = -1*math.cos(angle)*radius*0.4 + posx
    y = math.sin(angle)*radius + posy
    vertices[counter] = [x,y]

# Request a buffer slot from GPU
buffer = glGenBuffers(1)
# Make this buffer the default one
glBindBuffer(GL_ARRAY_BUFFER, buffer)

# Upload data
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER, buffer)

# Bind the position attribute
# --------------------------------------
stride = vertices.strides[0]
offset = ctypes.c_void_p(0)

loc = glGetAttribLocation(program, "position")
glEnableVertexAttribArray(loc)

glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)

loc_color = glGetUniformLocation(program, "color")
R = 1.0
G = 0.0
B = 0.0

# tamanho
s_x = 1.0
s_y = 1.0
s_z = 1.0

# rotacao
rad = 0.0
s = math.sin(rad)
c = math.cos(rad)

# translacao
t_x = 0.0
t_y = 0.0
t_z = 0.0
    

def mouse_event(window,button,action,mods):
    print('[mouse event] button =',button)
    print('[mouse event] action =',action)
    print('[mouse event] mods =',mods)
    print('-------')
    global s_x, s_y, s_z
    if button == 0:
        if action == 1:
            s_x += 0.05
            s_y += 0.05
    if button == 1:
        if action == 1:
            s_x -= 0.05
            s_y -= 0.05
    
glfw.set_mouse_button_callback(window,mouse_event)

def key_event(window,key,scancode,action,mods):
    global rad, s, c, t_x, t_y, t_z
    if key == 263:
        rad += 0.05
        if rad >= (2 * math.pi): rad = rad - (2 * math.pi)
        s = math.sin(rad)
        c = math.cos(rad)
    if key == 262:
        rad -= 0.05
        if rad < 0: rad = (2 * math.pi) + rad
        s = math.sin(rad)
        c = math.cos(rad)
    if key == 87: t_y += 0.05 #cima
    if key == 83: t_y -= 0.05 #baixo
    if key == 65: t_x -= 0.05 #esquerda
    if key == 68: t_x += 0.05 #direita
    
glfw.set_key_callback(window,key_event)

glfw.show_window(window)

while not glfw.window_should_close(window):

    glfw.poll_events() 

    glClear(GL_COLOR_BUFFER_BIT) 
    glClearColor(1.0, 1.0, 1.0, 1.0)    
    
    #Draw Triangle
    mat_transformation = np.array([     s_x * c, -(s_x * s), 0.0, (s_x * c * t_x) - (s_x * s * t_y), 
                                        s_y * s, s_y * s_z, 0.0, (s_y * s * t_x) + (s_y * c * t_y), 
                                        0.0, 0.0, s_z, s_z * t_z, 
                                        0.0, 0.0, 0.0, 1.0], np.float32)
                                    
    loc = glGetUniformLocation(program, "mat_transformation")
    glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transformation)
    
    glUniform4f(loc_color, 0.678, 0.333, 0.118, 1.0)
    glDrawArrays(GL_TRIANGLE_FAN, 0, 7) # perfil

    glUniform4f(loc_color, 0.153, 0.188, 0.188, 1.0)
    glDrawArrays(GL_TRIANGLE_FAN, 7, 6) # cima

    glUniform4f(loc_color, 0.290, 0.498, 0.447, 1.0)
    glDrawArrays(GL_TRIANGLE_FAN, 13, 5) # azul direita
    glDrawArrays(GL_TRIANGLE_FAN, 18, 5) # azul esquerda

    glUniform4f(loc_color, 0.972, 0.898, 0.294, 1.0)
    glDrawArrays(GL_TRIANGLE_FAN, 23, 6) # contorno smile preto

    glUniform4f(loc_color, 0.647, 0.247, 0.117, 1.0)
    glDrawArrays(GL_TRIANGLE_FAN, 29, num_vertices) #carinha
    glDrawArrays(GL_TRIANGLE_FAN, 29 + num_vertices, num_vertices)
    glDrawArrays(GL_TRIANGLE_STRIP, 29 + 2 * num_vertices, 4)
    glDrawArrays(GL_TRIANGLE_STRIP, 33 + 2 * num_vertices, 4)
    glDrawArrays(GL_TRIANGLE_STRIP, 37 + 2 * num_vertices, 4)
    glDrawArrays(GL_TRIANGLE_STRIP, 41 + 2 * num_vertices, 4)

    glUniform4f(loc_color, 0.212, 0.231, 0.227, 1.0)
    glDrawArrays(GL_TRIANGLE_FAN, 45 + 2 * num_vertices, num_vertices)
    glDrawArrays(GL_TRIANGLE_FAN, 45 + 3 * num_vertices, num_vertices)

    glfw.swap_buffers(window)

glfw.terminate()