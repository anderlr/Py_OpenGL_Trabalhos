import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from utils.MeshRenderer import SpaceshipMesh
from constants.constants import *
from utils.utils import *

securityCameraRotation=380

TRANSLATIONS = [[0, 20, 0], [10, 40, 0], [20, 20, 0], [20, 0, 0], ]
coord_x = 0
coord_y = 0
final_coord = False

pygame.init()
display = (1280, 720)
screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.display.set_caption(SCREEN_NAME)

glEnable(GL_DEPTH_TEST)

glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])

sphere = gluNewQuadric() 

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)

glMatrixMode(GL_MODELVIEW)
gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1)
viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
glLoadIdentity()


TEXTURES = [read_texture(PURPLE), read_texture(YELLOW), read_texture(GREEN), read_texture(PINK)]

displayCenter = [screen.get_size()[i] // 2 for i in range(2)]
mouseMove = [0, 0]
pygame.mouse.set_pos(displayCenter)

up_down_angle = 0.0
paused = False
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                run = False
            if event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                paused = not paused
                pygame.mouse.set_pos(displayCenter) 
        if not paused: 
            if event.type == pygame.MOUSEMOTION:
                mouseMove = [event.pos[i] - displayCenter[i] for i in range(2)]
            pygame.mouse.set_pos(displayCenter)    

    if not paused:
        keypress = pygame.key.get_pressed()
    
        glLoadIdentity()

        up_down_angle += mouseMove[1]*0.1
        glRotatef(up_down_angle, 1.0, 0.0, 0.0)

        glPushMatrix()
        glLoadIdentity()

        if keypress[pygame.K_w]:
            glTranslatef(0,0,0.1)
        if keypress[pygame.K_s]:
            glTranslatef(0,0,-0.1)
        if keypress[pygame.K_d]:
            glTranslatef(-0.1,0,0)
        if keypress[pygame.K_a]:
            glTranslatef(0.1,0,0)

        glRotatef(mouseMove[0]*0.1, 0.0, 1.0, 0.0)

        glMultMatrixf(viewMatrix)
        viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        glPopMatrix()
        glMultMatrixf(viewMatrix)
        glLightfv(GL_LIGHT0, GL_POSITION, [1, -1, 1, 0])

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glClearColor(*SCREEN_BACKGROUND_COLOR)

        securityCameraRotation+=5

        qobj = gluQuadricTexture(sphere, GL_TRUE)
        for i in range(4):
            glPushMatrix()
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, TEXTURES[i])
            glTranslatef(*TRANSLATIONS[i])
            glRotate(securityCameraRotation,0,0,1)
            gluSphere(sphere, 1.5, 50, 500)
            glPopMatrix()

        if coord_x < 20 and coord_y == 0:
            coord_x = coord_x + 0.1
        elif coord_x >= 20 and coord_y >= 0:
            coord_y = coord_y + 0.1
        elif coord_x >= 20 and coord_y >= 20:
            coord_x = coord_x - 0.1
            coord_y = coord_y + 0.1

        glPushMatrix()
        glTranslatef(coord_x, coord_y, 5)
        glRotate(securityCameraRotation,0,0,0.4)
        SpaceshipMesh()
        glPopMatrix()

        gluDeleteQuadric(qobj)
        glDisable(GL_TEXTURE_2D)

        pygame.display.flip()
        pygame.time.wait(10)

pygame.quit()