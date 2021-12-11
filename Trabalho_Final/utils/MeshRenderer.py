from constants.constants import SPACESHIP_EDGES_VECTOR, SPACESHIP_FACES_VECTOR, SPACESHIP_VERTICES_VECTOR

from OpenGL.GL import *
from OpenGL.GLU import *

def SpaceshipMesh():

    glBegin(GL_LINES)

    for edge in SPACESHIP_EDGES_VECTOR:
        for vertex in edge:
            glVertex3fv(SPACESHIP_VERTICES_VECTOR[vertex])
            
    
    glEnd()

    # glBegin(GL_QUADS)
    # for face in SPACESHIP_FACES_VECTOR:
    #     x = 0
    #     for vertex in face:
    #         x += 1
    #         # glColor3fv(colors[x])
    #         glVertex3fv(SPACESHIP_VERTICES_VECTOR[vertex])
    # glEnd()

    # glBegin(GL_LINES)
    # for edge in SPACESHIP_EDGES_VECTOR:
    #     for vertex in edge:
    #         glVertex3fv(SPACESHIP_VERTICES_VECTOR[vertex])
    # glEnd()
