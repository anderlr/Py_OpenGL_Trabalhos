from constants.constants import SPACESHIP_EDGES_VECTOR, SPACESHIP_FACES_VECTOR, SPACESHIP_VERTICES_VECTOR

from OpenGL.GL import *
from OpenGL.GLU import *

def SpaceshipMesh():

    glBegin(GL_LINES)
    for edge in SPACESHIP_EDGES_VECTOR:
        x = 0
        for vertex in edge:
            x += 1
            glVertex3fv(SPACESHIP_VERTICES_VECTOR[vertex])
    glEnd()
