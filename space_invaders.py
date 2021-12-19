import os
from time import sleep
import random
from math import sqrt
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
from pywavefront import visualization

SHIP_X = 0
SHIP_Y = 0
SHIP_Z = 15

ENEMY_Z_WALK_DISTANCE = 0.3
INITIAL_ENEMY_Z_DISTANCE = -150

MISSILE_TRAVEL_DISTANCE = -1

MISSILE_ENEMY_COLLISION_DISTANCE = 10

def get_random_rgb_value():
    random_rgb_tuple = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
    return random_rgb_tuple

"""
X -> Horizontal
Y -> Altura 
Z -> Profundidade
"""
class Enemy:
    def __init__(self, x, y, z, color):
        """
        x -> X position of Enemy
        y -> Y position of Enemy
        z -> Z position of Enemy
        alive -> 'Alive' state of Enemy
        color -> 'Color' state of Enemy
        """
        self.x = x
        self.y = y
        self.z = z
        self.color = color
        self.alive = True
    
    def move(self):
        self.z += ENEMY_Z_WALK_DISTANCE


class Missile:
    def __init__(self, x, y, z):
        """
        x -> X position of Missile
        y -> Y position of Missile
        z -> Z position of Missile
        """
        self.x = x
        self.y = y
        self.z = z
    
    def move(self):
        self.z += MISSILE_TRAVEL_DISTANCE


# Initial enemy list
first_random_color = get_random_rgb_value()
enemy_list = [
    Enemy(1.2, 1, INITIAL_ENEMY_Z_DISTANCE, first_random_color),
    Enemy(20.2, 1, INITIAL_ENEMY_Z_DISTANCE, first_random_color),
    Enemy(-20.2, 1, INITIAL_ENEMY_Z_DISTANCE, first_random_color)
]

missile_list = []

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()


    #Ações em toda a nave
    #glRotatef(T, 0.0, 1.0, 0.0)
    
    #glScalef(T, T2, T3)

    glPushMatrix()
    #Corpo da nave
    glTranslatef(SHIP_X, SHIP_Y, SHIP_Z)
    glColor3f(0.0, 0.0, 1.0)
    glRotated(180, 1, 0, 0)
    visualization.draw(nave)
    glPopMatrix()



    alive_enemies = [enemy for enemy in enemy_list if enemy.alive]

    for enemy in alive_enemies:
        enemy.move()
        glPushMatrix()
        glColor3f(enemy.color[0], enemy.color[1], enemy.color[2])
        glTranslatef(enemy.x, enemy.y, enemy.z)
        visualization.draw(invasor)
        glPopMatrix()
    
    destroyed_missiles = []

    for index, missile in enumerate(missile_list):
        for alive_enemy in alive_enemies:
            missile_enemy_distance = sqrt((missile.x - alive_enemy.x)**2 + (missile.z - alive_enemy.z)**2)
            if missile_enemy_distance <= MISSILE_ENEMY_COLLISION_DISTANCE:
                alive_enemy.alive = False
                destroyed_missiles.append(index)
        missile.move()
        glPushMatrix()
        random_missile_color = get_random_rgb_value()
        glColor3f(random_missile_color[0], random_missile_color[1], random_missile_color[2])
        glTranslatef(missile.x, missile.y, missile.z)
        visualization.draw(missel)
        glPopMatrix()

    for missiles_to_destroy in destroyed_missiles:
        missile_list.pop(missiles_to_destroy)

    glPopMatrix()
    


    glutSwapBuffers()


def TreatKeyboardKeys(key, x, y):
    global SHIP_X
    if key == b's':
        missile_list.append(Missile(SHIP_X, SHIP_Y, SHIP_Z))
    if(key == b'a' ):
        SHIP_X -= 3 
    elif(key == b'd' ): 
        SHIP_X += 3
       
def animacao(value):
    glutPostRedisplay()
    glutTimerFunc(30, animacao,1)

def add_enemies(value):
    first_x_value = random.choice((5.2, -10.2))
    second_x_value = random.choice((20.2, -20.2))
    third_x_value = random.choice((30.2, -30.2))
    randomized_color = get_random_rgb_value()
    enemy_list.append(Enemy(first_x_value, 1, INITIAL_ENEMY_Z_DISTANCE, randomized_color))
    enemy_list.append(Enemy(second_x_value, 1, INITIAL_ENEMY_Z_DISTANCE, randomized_color))
    enemy_list.append(Enemy(third_x_value, 1, INITIAL_ENEMY_Z_DISTANCE, randomized_color))
    glutTimerFunc(1000, add_enemies, 1)

    
def resize(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(65.0, w/h, 1.0, 200.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 20.0, 35.0,
                0.0, 3.0, -10.0,
                0.0, 1.0, 0.0)

  

def init():
    glClearColor (0.3, 0.3, 0.3, 0.0)
    glShadeModel( GL_SMOOTH )
    glClearColor( 0.0, 0.1, 0.0, 0.5 )
    glClearDepth( 1.0 )
    glEnable( GL_DEPTH_TEST )
    glDepthFunc( GL_LEQUAL )
    glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )

    glLightModelfv( GL_LIGHT_MODEL_AMBIENT, [0.3, 0.3, 0.3, 1.0] )
    glLightfv( GL_LIGHT0, GL_AMBIENT, [ 0.6, 0.6, 0.6, 1.0] )
    glLightfv( GL_LIGHT0, GL_DIFFUSE, [0.7, 0.7, 0.7, 1.0] )
    glLightfv( GL_LIGHT0, GL_SPECULAR, [0.7, 0.7, 0.7, 1] )
    glLightfv( GL_LIGHT0, GL_POSITION, [2.0, 2.0, 1.0, 0.0])
    glEnable( GL_LIGHT0 )
    glEnable( GL_COLOR_MATERIAL )
    glShadeModel( GL_SMOOTH )
    glLightModeli( GL_LIGHT_MODEL_TWO_SIDE, GL_FALSE )
    glDepthFunc( GL_LEQUAL )
    glEnable( GL_DEPTH_TEST )
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

glutInit()
assets = os.path.join(os.getcwd(), "assets")
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(1920, 1080)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow("Space Invaders")
init()
nave = pywavefront.Wavefront(os.path.join(assets, "spaceship.obj"))
missel = pywavefront.Wavefront(os.path.join(assets, "missile.obj"))
invasor = pywavefront.Wavefront(os.path.join(assets, "new_invader.obj"))
glutDisplayFunc(display)
glutReshapeFunc(resize)
glutTimerFunc(30,animacao,1)
glutTimerFunc(1000, add_enemies ,1)
glutKeyboardFunc(TreatKeyboardKeys)
#glutKeyboardUpFunc(Keys_letras_soltar)
glutMainLoop()
