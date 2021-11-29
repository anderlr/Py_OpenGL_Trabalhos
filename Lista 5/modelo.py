'''
Trabalho para a Lista 5
Douglas Raimundo de Oliveira Silva - 2019018540
Gabriel  Jose Mouallem Rodrigues - 2017017731
Anderson Leandro Dos Reis - 2018019033

'''

import sys
from OpenGL.raw.GL.VERSION.GL_1_0 import GL_FRONT_AND_BACK, GL_LINE
from OpenGL.raw.GL.VERSION.GL_1_5 import GL_ELEMENT_ARRAY_BUFFER
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut
from ctypes import c_void_p
import utils as ut

from numpy.lib.function_base import angle

# contador de teclas
key_counter = 0

# opcao inicial
option = 't'
# Largura da Janela
win_width = 800
# Altura da Janela
win_height = 600

# Variavel Program
program = None
# Vertex array object.
VAO = None
# Vertex buffer object.
VBO = None
# Index buffer objetct
EBO = None


# Vertex shader.
vertex_code = """
#version 330 core
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 color;

out vec3 vColor;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    gl_Position = projection * view * model * vec4(position, 1.0);
    vColor = color;
}
"""

# Fragment shader.
fragment_code = """
#version 330 core

in vec3 vColor;
out vec4 FragColor;

void main()
{
    FragColor = vec4(vColor, 1.0f);
} 
"""


def display():

    gl.glClearColor(0.2, 0.3, 0.3, 1.0)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    gl.glUseProgram(program)
    gl.glBindVertexArray(VAO)

    # Define model matrix.
    Rx = ut.matRotateX(np.radians(0.0))
    T = ut.matTranslate(0.0, 0.0, -10.0)
    model = np.matmul(T, Rx)

    # Retrieve location of model variable in shader.
    loc = gl.glGetUniformLocation(program, "model")
    # Send matrix to shader.
    gl.glUniformMatrix4fv(loc, 1, gl.GL_FALSE, model.transpose())

    # Define view matrix.
    view = ut.matTranslate(0.0, 0.0, 0.0)

    # Retrieve location of view variable in shader.
    loc = gl.glGetUniformLocation(program, "view")
    # Send matrix to shader.
    gl.glUniformMatrix4fv(loc, 1, gl.GL_FALSE, view.transpose())

    # Define projection matrix.
    projection = ut.matPerspective(np.radians(
        30), win_width/win_height, 0.1, 100.0)

    # Retrieve location of projection variable in shader.
    loc = gl.glGetUniformLocation(program, "projection")
    # Send matrix to shader.
    gl.glUniformMatrix4fv(loc, 1, gl.GL_FALSE, projection.transpose())

    # Draws the triangle.
    gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6 * total_pixels)

    glut.glutSwapBuffers()


# Reshape function.
#
# Called when window is resized.
#
# @param width New window width.
# @param height New window height.
def reshape(width, height):
    gl.glViewport(0, 0, width, height)
    glut.glutPostRedisplay()


# Keyboard function.
#
# Called to treat pressed keys.
#
# @param key Pressed key.
# @param x Mouse x coordinate when key pressed.
# @param y Mouse y coordinate when key pressed.
def keyboard(key, x, y):

    global key_counter
    global option

    # change type of drawing
    if key == b'v' and key_counter == 0:
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_POINT)
        key_counter = 1
    elif key == b'v' and key_counter == 1:
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        key_counter = 2
    elif key == b'v' and key_counter == 2:
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
        key_counter = 0

    # change option
    if key == b't':  # translation
        option = 't'
    elif key == b'r':  # rotation
        option = 'r'
    elif key == b'e':  # scale
        option = 'e'

    if option == 't':
        if key == b'w':
            vertices[:, 1] = vertices[:, 1] + 0.025
        elif key == b's':
            vertices[:, 1] = vertices[:, 1] - 0.025
        elif key == b'd':
            vertices[:, 0] = vertices[:, 0] + 0.025
        elif key == b'a':
            vertices[:, 0] = vertices[:, 0] - 0.025
        elif key == b'd':
            vertices[:, 0] = vertices[:, 0] + 0.025
        elif key == b'p':
            vertices[:, 2] = vertices[:, 2] + 0.025
        elif key == b'n':
            vertices[:, 2] = vertices[:, 2] - 0.025

    elif option == 'r':
        if key == b'p':  # giro em torno de z +
            vertices[:, 0] = vertices[:, 0] * \
                np.cos(0.01) + vertices[:, 1] * np.sin(0.01)
            vertices[:, 1] = vertices[:, 1] * \
                np.cos(0.01) - vertices[:, 0] * np.sin(0.01)
        elif key == b'n':  # giro em torno de z -
            vertices[:, 0] = vertices[:, 0] * \
                np.cos(-0.01) + vertices[:, 1] * np.sin(-0.01)
            vertices[:, 1] = vertices[:, 1] * \
                np.cos(-0.01) - vertices[:, 0] * np.sin(-0.01)
        elif key == b'd':  # giro em torno de x +
            vertices[:, 1] = vertices[:, 1] * \
                np.cos(0.01) + vertices[:, 2] * np.sin(0.01)
            vertices[:, 2] = vertices[:, 2] * \
                np.cos(0.01) - vertices[:, 1] * np.sin(0.01)
        elif key == b'a':  # giro em torno de x -
            vertices[:, 1] = vertices[:, 1] * \
                np.cos(-0.01) + vertices[:, 2] * np.sin(-0.01)
            vertices[:, 2] = vertices[:, 2] * \
                np.cos(-0.01) - vertices[:, 1] * np.sin(-0.01)
        elif key == b'w':  # giro em torno de y +
            vertices[:, 0] = vertices[:, 0] * \
                np.cos(0.01) + vertices[:, 2] * np.sin(0.01)
            vertices[:, 2] = vertices[:, 2] * \
                np.cos(0.01) - vertices[:, 0] * np.sin(0.01)
        elif key == b's':  # giro em torno de y +
            vertices[:, 0] = vertices[:, 0] * \
                np.cos(-0.01) + vertices[:, 2] * np.sin(-0.01)
            vertices[:, 2] = vertices[:, 2] * \
                np.cos(-0.01) - vertices[:, 0] * np.sin(-0.01)

    elif option == 'e':
        if key == b'w':
            vertices[:, 1] = vertices[:, 1] * 1.025
        elif key == b's':
            vertices[:, 1] = vertices[:, 1] / 1.025
        elif key == b'd':
            vertices[:, 0] = vertices[:, 0] * 1.025
        elif key == b'a':
            vertices[:, 0] = vertices[:, 0] / 1.025
        elif key == b'p':
            vertices[:, 2] = vertices[:, 2] * 1.025
        elif key == b'n':
            vertices[:, 2] = vertices[:, 2] / 1.025

    # reset
    if key == b'm':
        vertices[:, :] = create_image()

    initData(vertices)
    glut.glutPostRedisplay()


def ppm_to_array(filedirectory):

    # read dimension of a ppm file, return the dimension and the matrix of the image

    with open(filedirectory, 'r') as file:
        img_read = file.read().split('\n')
        dimension = np.array(img_read[1].split(), dtype=int)
        img = list(map(lambda x: x.split(), img_read[3:]))[:-1]
    return dimension[0], dimension[1], np.array(img, dtype=int)

# Init vertex data.
#
# Defines the coordinates for vertices, creates the arrays for OpenGL.


def create_square(dimensionX, dimensionY, deslX=0, deslY=0, colors=(1.0, 1.0, 1.0)):
    vertices = np.array([

        # first triangle
        dimensionX + deslX, dimensionY + \
        deslY, 0.0, colors[0], colors[1], colors[2],  # top right
        dimensionX + deslX, -dimensionY + \
        deslY, 0.0, colors[0], colors[1], colors[2],  # bottom right
        -dimensionX + deslX, dimensionY + \
        deslY, 0.0, colors[0], colors[1], colors[2],  # top left
        # second triangle
        dimensionX + deslX, -dimensionY + \
        deslY, 0.0, colors[0], colors[1], colors[2],  # bottom right
        -dimensionX + deslX, -dimensionY + \
        deslY, 0.0, colors[0], colors[1], colors[2],  # bottom left
        -dimensionX + deslX,  dimensionY + \
        deslY, 0.0, colors[0], colors[1], colors[2],  # top left

    ], dtype='float32')

    return vertices


def create_image():

    # x dimension and y dimension
    dimensionX = 1 / numPixelsX - 0.00001
    dimensionY = 1 / numPixelsY - 0.00001

    # creating a vertices array
    colors = np.apply_along_axis(
        arr=img, func1d=lambda x: np.split(x, numPixelsX), axis=1)
    colors = colors / 255

    # creating squares with vertices_positions and colors

    vertices_positions = []
    for i, img_i in zip(range(-numPixelsX + 1, numPixelsX + 1, 2), range(numPixelsX - 1, -1, -1)):
        for j, img_j in zip(range(-numPixelsY + 1, numPixelsY + 1, 2), range(0, numPixelsY)):
            vertices_positions.append((j, i, img_i, img_j))
    vertices = [create_square(dimensionX, dimensionY, i * dimensionX, j * dimensionY,
                              colors=colors[img_i, img_j]) for i, j, img_i, img_j in vertices_positions]

    # concatenate all vertices
    vertices = np.concatenate(vertices, axis=0)
    vertices = np.array(vertices).reshape(len(vertices)//6, 6)

    # Ajustando escala inicial
    vertices[:, 0] = vertices[:, 0] / 1.25
    vertices[:, 1] = vertices[:, 1] / 1.25
    vertices[:, 2] = vertices[:, 2] / 1.25

    return vertices


def initData(vertices):

    # Uses vertex arrays.
    global VAO
    global VBO

    # indexes = np.array([
    #     0, 1, 3,  # first Triangle
    #     1, 2, 3   # second Triangle
    # ], dtype='float32')

    gl.glEnable(gl.GL_DEPTH_TEST)

    # Vertex array.
    VAO = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(VAO)

    # Vertex buffer
    VBO = gl.glGenBuffers(1)
    # EBO = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes,
                    vertices, gl.GL_STATIC_DRAW)

    # gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, EBO)
    # gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes,indices, gl.GL_STATIC_DRAW)

    # Set attributes, declarando que a cor vem depois de cada vertice

    gl.glVertexAttribPointer(
        0, 3, gl.GL_FLOAT, gl.GL_FALSE, 6*vertices.itemsize, None)
    gl.glEnableVertexAttribArray(0)
    gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE,
                             6*vertices.itemsize, c_void_p(3*vertices.itemsize))
    gl.glEnableVertexAttribArray(1)

    # Unbind Vertex Array Object.
    gl.glBindVertexArray(0)


# Create program (shaders).
#
# Compile shaders and create the program.


def initShaders():

    # Uses vertex arrays.
    global program

    # Request a program and shader slots from GPU
    program = gl.glCreateProgram()
    vertex = gl.glCreateShader(gl.GL_VERTEX_SHADER)
    fragment = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)

    # Set shaders source
    gl.glShaderSource(vertex, vertex_code)
    gl.glShaderSource(fragment, fragment_code)

    # Compile shaders
    gl.glCompileShader(vertex)
    gl.glCompileShader(fragment)

    # Attach shader objects to the program
    gl.glAttachShader(program, vertex)
    gl.glAttachShader(program, fragment)

    # Link the program
    gl.glLinkProgram(program)

    # Get rid of shaders (not needed anymore)
    gl.glDetachShader(program, vertex)
    gl.glDetachShader(program, fragment)
    gl.glDeleteShader(vertex)
    gl.glDeleteShader(fragment)

    # Set the program to be used.
    gl.glUseProgram(program)

# Main function.
#
# Init GLUT and the window settings. Also, defines the callback functions used in the program.


def main():

    # Memory Allocation
    global numPixelsX, numPixelsY, total_pixels, img
    global vertices

    numPixelsX, numPixelsY, img = ppm_to_array(sys.argv[1])
    total_pixels = numPixelsX * numPixelsY

    glut.glutInit()
    glut.glutInitContextVersion(3, 3)
    glut.glutInitContextProfile(glut.GLUT_CORE_PROFILE)
    glut.glutInitDisplayMode(
        glut.GLUT_DOUBLE | glut.GLUT_RGBA | glut.GLUT_DEPTH)
    glut.glutInitWindowSize(win_width, win_height)
    glut.glutCreateWindow('Triangle')

    # Init vertex data for the triangle.
    vertices = create_image()
    initData(vertices)

    # Create shaders.
    initShaders()

    glut.glutReshapeFunc(reshape)
    glut.glutDisplayFunc(display)
    glut.glutKeyboardFunc(keyboard)

    glut.glutMainLoop()


if __name__ == '__main__':
    main()

# https://learnopengl.com/Getting-started/Hello-Triangle
