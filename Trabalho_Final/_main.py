import pygame
import random
import os

from OpenGL.GL import *
from OpenGL.GLU import *

from pygame.locals import *
from constants.constants import SPACESHIP_EDGES_VECTOR, SPACESHIP_FACES_VECTOR, SPACESHIP_VERTICES_VECTOR
from utils.MeshRenderer import SpaceshipMesh

os.environ["SDL_VIDEO_CENTERED"] = '1'

def random_color():
    x = random.randint(0, 255)/255
    y = random.randint(0, 255)/255
    z = random.randint(0, 255)/255
    color = (x, y, z)
    return color

colors_list = []

def main():
    pygame.init()
    display = (1000, 1000)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslate(0.0, 0, -20)
    glRotatef(-90, 2, 0, 0)

main()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    glRotatef(4, 3, -10, -45)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    SpaceshipMesh()
    pygame.display.flip()
    pygame.time.wait(10)
pygame.quit()
quit()