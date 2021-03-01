import PyGL
from PyGL.core.renderers import Renderer
from PyGL.core.lights import BasicLight
from PyGL.core import cameras
import pygame
import numpy
from pathlib import Path

print("PyGL version:", PyGL.__version__)

size = (720, 1280)

pygame.init()

screen = pygame.display.set_mode((size[1], size[0]))

clock = pygame.time.Clock()
FPS = 100
scene = PyGL.Scene(size)

in_path = Path.cwd() / "objects" / "cube.obj"

cube = scene.load_obj(in_path)
cube.scale = 100
cube.pos[0] = size[1] / 2
cube.pos[1] = size[0] / 2
#cube.rotation[1] = 30
#cube.rotation[2] = 100
#cube.rotation[0] = 20

renderer = Renderer(screen)

lights = []
light = BasicLight.Light()
light.normal[2] = -1
light.pos[2] = -1
lights.append(light)

camera = cameras.Camera()
camera.configure()

delta_time = 1/FPS

#renderer.render(scene, camera, lights)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    cube.rotation[0] += 50 * delta_time
    cube.rotation[1] += 60 * delta_time
    cube.rotation[2] += 70 * delta_time

    renderer.render(scene, camera, lights)

    fps = float(int(clock.get_fps()))
    print("FPS:",fps, end="\r")
    clock.tick(FPS)

pygame.quit()
