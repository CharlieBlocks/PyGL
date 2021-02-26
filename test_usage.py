import PyGL
import pygame
import numpy as np
import time
from pathlib import Path 


width = 1280
height = 720

pygame.init()

width, height = 1280, 720
screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()
scene = PyGL.Scene(screen)
font = pygame.font.SysFont("Arial", 18)

FPS = 120

fps_history = []

inpath = Path.cwd() / "cube.obj"

vertices = np.array([[0, 0, 0], [1, 0, 1], [1, 0, 0]])
#trig = scene.add_triangle_from_array(vertices)
trig = scene.load_obj(inpath, False)
trig.scale = 100
trig.pos.point[0] = width/2
trig.pos.point[1] = height/2
renderer = PyGL.Basic_Renderer(screen)

delta_time = 1

trig.rot[0] += 50
trig.rot[2] += 30
trig.rot[1] += 70

running = True 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    trig.rot[0] += 20 * delta_time
    trig.rot[2] += 25 * delta_time
    trig.rot[1] += 15 * delta_time
    

    scene.update(renderer)
    fps = float(int(clock.get_fps()))
    try:
        delta_time = 1/fps
    except:
        delta_time = 1/FPS

    print("FPS:",fps, end="\r")
    clock.tick(FPS)


def update():
    scene.update(renderer)


pygame.quit()