'''
Trabalho para a Avaliação (N1)
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


def ppm_to_array(filedirectory):

    # read dimension of a ppm file, return the dimension and the matrix of the image

    with open(filedirectory, 'r') as file:
        img_read = file.read().split('\n')
        dimension = np.array(img_read[1].split(), dtype = int)
        # img = list(map(lambda x: x.split(), img_read[3:]))[:-1]
    
    return dimension[0], dimension[1] #, np.array(img, dtype = int)


## Largura da Janela
win_width = 800
## Altura da Janela
win_height = 600

## Variavel Program
program = None
## Vertex array object.
VAO = None
## Vertex buffer object.
VBO = None
##Index buffer objetct
EBO = None



## Vertex shader.
vertex_code = """
#version 330 core
layout (location = 0) in vec3 position;

void main()
{
    gl_Position = vec4(position.x, position.y, position.z, 1.0);
}
"""

## Fragment shader.
fragment_code = """
#version 330 core
out vec4 FragColor;

void main()
{
    FragColor = vec4(1.0f, 1.0f, 1.0f, 1.0f);
} 
"""

def display():

    gl.glClearColor(0.0, 0.0, 0.0, 1.0)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    gl.glUseProgram(program)
    gl.glBindVertexArray(VAO)
    # Draws the triangle.
    gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6 * total_pixels)

    glut.glutSwapBuffers()


## Reshape function.
#
# Called when window is resized.
#
# @param width New window width.
# @param height New window height.
def reshape(width, height):

    win_width = width
    win_height = height
    gl.glViewport(0, 0, width, height)
    glut.glutPostRedisplay()


## Keyboard function.
#
# Called to treat pressed keys.
#
# @param key Pressed key.
# @param x Mouse x coordinate when key pressed.
# @param y Mouse y coordinate when key pressed.
def keyboard(key, x, y):

    if key == b'\x1b' or key == b'q':
        sys.exit()


## Init vertex data.
#
# Defines the coordinates for vertices, creates the arrays for OpenGL.

def create_square(dimensionX, dimensionY, deslX = 0, deslY = 0):
    vertices = np.array([

        # first triangle
        dimensionX + deslX, dimensionY + deslY, 0.0,  # top right
        dimensionX + deslX, -dimensionY + deslY, 0.0,  # bottom right
        -dimensionX + deslX, dimensionY + deslY, 0.0,  # top left
        # second triangle
        dimensionX + deslX, -dimensionY + deslY, 0.0,  # bottom right
        -dimensionX + deslX, -dimensionY + deslY, 0.0,  # bottom left
        -dimensionX + deslX,  dimensionY + deslY, 0.0,  # top left

    ], dtype = 'float32')

    return vertices

def initData():

    # Uses vertex arrays.
    global VAO
    global VBO

    # x dimension and y dimension
    dimensionX = 1 / numPixelsX - 0.00001
    dimensionY = 1 / numPixelsY - 0.00001

    # creating vertices array and squares
    vertices_positions = [(i, j) for j in range(-numPixelsY + 1, numPixelsY + 1, 2) for i in range(-numPixelsX + 1, numPixelsX + 1, 2)]
    vertices = [create_square(dimensionX, dimensionY, i * dimensionX, j * dimensionY) for i, j in vertices_positions]

    # concatenate all vertices
    vertices = np.concatenate(vertices, axis = 0)

    # Vertex array.
    VAO = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(VAO)

    # Vertex buffer
    VBO = gl.glGenBuffers(1)
    # EBO = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW)

    # gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, EBO)
    # gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes,indices, gl.GL_STATIC_DRAW)

    # Set attributes.
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
    gl.glEnableVertexAttribArray(0)

    # Unbind Vertex Array Object.
    gl.glBindVertexArray(0)

    #Setting the draw mode to line
    gl.glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)

## Create program (shaders).
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
    


## Main function.
#
# Init GLUT and the window settings. Also, defines the callback functions used in the program.
def main():

    ## Memory Allocation
    global numPixelsX, numPixelsY, total_pixels
    numPixelsX, numPixelsY = ppm_to_array(sys.argv[1])
    total_pixels = numPixelsX * numPixelsY

    glut.glutInit()
    glut.glutInitContextVersion(3, 3)
    glut.glutInitContextProfile(glut.GLUT_CORE_PROFILE)
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)
    glut.glutInitWindowSize(win_width, win_height)
    glut.glutCreateWindow('Triangle')

    # Init vertex data for the triangle.
    initData()

    # Create shaders.
    initShaders()

    glut.glutReshapeFunc(reshape)
    glut.glutDisplayFunc(display)
    glut.glutKeyboardFunc(keyboard)

    glut.glutMainLoop()


if __name__ == '__main__':
    main()


# https://learnopengl.com/Getting-started/Hello-Triangle
