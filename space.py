import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import random
import cv2
face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
ret = cap.set(3,400)
ret=cap.set(4,300)
display = (1200,600)
white=(255,255,255)
black=(0,0,0)
green=(0,200,0)
red=(200,0,0)
b_green=(0,255,0)
b_red=(255,0,0)

pygame.init()
clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode(display)

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

colors = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 1, 0),
    (1, 1, 1),
    (0, 1, 1),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 0, 0),
    (1, 1, 1),
    (0, 1, 1),
)

def set_vertices(max_distance, min_distance=-20, camera_x=0, camera_y=0):
    camera_x = -1 * int(camera_x)
    camera_y = -1 * int(camera_y)

    x_value_change = random.randrange(camera_x - 30, camera_x + 30)
    y_value_change = random.randrange(camera_y + 0, camera_y + 1)

    z_value_change = random.randrange(-1 * max_distance, min_distance)

    new_vertices = []

    for vert in vertices:
        new_vert = []

        new_x = vert[0] + x_value_change
        new_y = vert[1] + y_value_change
        new_z = vert[2] + z_value_change

        new_vert.append(new_x)
        new_vert.append(new_y)
        new_vert.append(new_z)

        new_vertices.append(new_vert)

    return new_vertices


def Cube(vertices):
    glBegin(GL_QUADS)

    for surface in surfaces:
        x = 0

        for vertex in surface:
            x += 1
            glColor3fv(colors[x])
            glVertex3fv(vertices[vertex])

    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def textobjects(text,font,colo):
    textSurface=font.render(text,True,colo)
    return textSurface,textSurface.get_rect()

def button(msg,colo,fon,siz,x,y,w,h,ic,ac,action):
    mouse = pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if x+w/2 > mouse[0] > x-w/2 and y + h/2 > mouse[1] > y-h/2:
        if click[0]==1:
            if action=='play':
                main()

        pygame.draw.rect(gameDisplay, ac, (x-w/2, y-h/2, w, h))
    else:
        pygame.draw.rect(gameDisplay, ic, (x-w/2, y-h/2, w, h))
    smallText = pygame.font.Font(fon, siz)
    TextSurf, TextRect = textobjects(msg, smallText,colo)
    TextRect.center = (x,y)
    gameDisplay.blit(TextSurf, TextRect)

def Cap(msg,fon,siz,colo):
    bigText=pygame.font.Font(fon,siz)
    TextSurf, TextRect = textobjects(msg, bigText, colo)
    TextRect.center = (display[0]/2, display[1]/2)
    gameDisplay.blit(TextSurf, TextRect)



def game_intro():
    pygame.init()
    clock = pygame.time.Clock()
    gameDisplay = pygame.display.set_mode(display)
    #img = pygame.image.load('image\space.jpg')
    icon = pygame.image.load('image\iconspace.jpg')
    pygame.display.set_caption('Space')
    pygame.display.set_icon(icon)
    intro=True
    while intro :
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                quit()
        Cap('SPACE','Font\intro.ttf',100,white)
        button('PLAY',black,'Font\intro.ttf',20,600,500,100,50,(0,20,0),white,"play")
        pygame.display.update()
        clock.tick(15)
pause=True
def game_pause():
    pygame.init()
    clock = pygame.time.Clock()
    gameDisplay = pygame.display.set_mode(display)
    global pause
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        bigText = pygame.font.Font('Font\intro.ttf', 80)
        TextSurf, TextRect = textobjects('PAUSE', bigText, white)
        TextRect.center = (display[0] / 2, display[1] / 2)
        gameDisplay.blit(TextSurf, TextRect)

        pygame.display.update()
        clock.tick(15)

def main():
    pygame.init()
    pygame.time.Clock()
    display = (1200, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    max_distance = 100

    gluPerspective(45, (display[0] / display[1]),0.1, max_distance)

    glTranslatef(0, 0, -40)

    # object_passed = False
    x_move = 0
    y_move = 0

    cur_x = 0
    cur_y = 0

    game_speed = 1
    direction_speed = 1

    cube_dict = {}
    bien = 0

    for x in range(50):
        cube_dict[x] = set_vertices(max_distance)
    #main_sound=pygame.mixer.Sound('sound\space.wav')
    #pygame.mixer.Sound.play(main_sound)

    while True:

        ret, img = cap.read(0)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #pygame.mixer.Sound.play(main_sound)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
        cv2.imshow('CAM', img)

        if len(faces)!=0:
#
            if faces[0][0]>(bien+2):
                x_move=direction_speed
            elif faces[0][0]<(bien-2):
                x_move=-1*direction_speed
            else:
                x_move=0
            bien=faces[0][0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_move = direction_speed
                if event.key == pygame.K_RIGHT:
                    x_move = -1 * direction_speed

                if event.key == pygame.K_UP:
                    y_move = -1 * direction_speed
                if event.key == pygame.K_DOWN:
                    y_move = direction_speed
                if event.key==pygame.K_SPACE:
                    game_pause()


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_move = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_move = 0
        x = glGetDoublev(GL_MODELVIEW_MATRIX)
        camera_z = x[3][2]

        cur_x += x_move
        cur_y += y_move

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glTranslatef(x_move, y_move, game_speed)

        for each_cube in cube_dict:
            Cube(cube_dict[each_cube])

        for each_cube in cube_dict:
            if camera_z <= cube_dict[each_cube][0][2]:
                new_max = int(-1 * (camera_z - (max_distance * 2)))
                cube_dict[each_cube] = set_vertices(new_max, int(camera_z - max_distance), cur_x, cur_y)

        pygame.display.flip()

game_intro()
main()
pygame.time.get_ticks(30)
pygame.quit()
quit()