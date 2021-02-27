import copy
from ..maths import *
import pygame

class Renderer:
    def __init__(self, screen): #Takes a pygame screen object
        self.screen = screen
        self.projection_matrix = np.zeros((4,4))
        self.last_camera_pos = 0
        self.last_camera_lookDirection = 0
        self.last_camera_fov = 0

        self.colour = [255, 255, 255]

        self._init = False

    def _from_rgb(self, rgb):
        """translates an rgb tuple of int to a tkinter friendly color code
        """
        return "#%02x%02x%02x" % rgb   

    def draw(self):
        self.screen.fill("black")
        #pygame.display.flip()
        for tri in self.to_draw:
            RGB = (int(tri.r), int(tri.g), int(tri.b))

            colour = self._from_rgb(RGB)
            
            #print((tri.p[0][0], tri.p[0][1]), (tri.p[1][0], tri.p[1][1]), (tri.p[2][0], tri.p[2][1]))
            pygame.draw.polygon(self.screen, colour, ((tri.p[0][0], tri.p[0][1]), (tri.p[1][0], tri.p[1][1]), (tri.p[2][0], tri.p[2][1])))
        pygame.display.flip()

    def render(self, scene, camera, lights): 
        #Takes the following args
        #   A PyGL scene object
        #   A PyGL camera object
        #   A list/numpy array of lights from PyGL.core.lights either complex or basic

        self.to_draw = [] #Sets up an array for the triangles to be stored in.


        if not np.array_equal(self.last_camera_pos, camera.pos) or not np.array_equal(self.last_camera_lookDirection, camera.look_direction) or not self._init:

            #Only recreates a camera matrix if the camera values have been changed
            camera.create_matrix() #A built-in function of the camera object

            self._init = True #Set variables to current values
            self.last_camera_pos = camera.pos
            self.last_camera_lookDirection = camera.look_direction
        
        if self.last_camera_fov != camera.fFov: #Creates a new projection matrix if a camera value changes

            self.projection_matrix[0][0] = camera.fAspectRatio * camera.fFovRad
            self.projection_matrix[1][1] = camera.fFovRad
            self.projection_matrix[2][2] = camera.fFar / (camera.fFar - camera.fNear)
            self.projection_matrix[3][2] = (-camera.fFar * camera.fNear) / (camera.fFar - camera.fNear)
            self.projection_matrix[2][3] = 1
            self.projection_matrix[3][3] = 0

            self.last_camera_fov = camera.fFov

        
        for j in scene.objects:   #Get's each mesh object from the list passed to it

            create_rotation_matrix(j.rot_mat, j.rotation[0], j.rotation[1], j.rotation[2])

            for i in j.m:   # Gets each triangle from the mesh object
                tri = copy.deepcopy(i)
                
                tri.p[0] = multiply_matrix(camera.camera_matrix, tri.p[0])
                tri.p[1] = multiply_matrix(camera.camera_matrix, tri.p[1])
                tri.p[2] = multiply_matrix(camera.camera_matrix, tri.p[2])

                tri.p[0] = multiply_matrix(j.rot_mat, tri.p[0])
                tri.p[1] = multiply_matrix(j.rot_mat, tri.p[1])
                tri.p[2] = multiply_matrix(j.rot_mat, tri.p[2])
                tri.normal = multiply_matrix(j.rot_mat, tri.normal)

                if tri.normal[2] < 0:
                    scale_vector(tri.p[0], j.scale) #Scale triangle
                    scale_vector(tri.p[1], j.scale)
                    scale_vector(tri.p[2], j.scale)

                    translate_vector(tri.p[0], j.pos[0], j.pos[1], j.pos[2]) #Translate the triangle in 3D space
                    translate_vector(tri.p[1], j.pos[0], j.pos[1], j.pos[2])
                    translate_vector(tri.p[2], j.pos[0], j.pos[1], j.pos[2])

                    tri.p[0] = multiply_matrix(self.projection_matrix, tri.p[0]) 
                    tri.p[1] = multiply_matrix(self.projection_matrix, tri.p[1])
                    tri.p[2] = multiply_matrix(self.projection_matrix, tri.p[2])          


                    for light in lights:
                        if not light.custom_script:
                            dp = vector_dot_product(tri.normal, light.normal)

                            tri.r = abs(min(255, self.colour[0]*dp))
                            tri.g = abs(min(255, self.colour[1]*dp))
                            tri.b = abs(min(255, self.colour[2]*dp))

                            tri.r = max(0, min(255, tri.r))
                            tri.g = max(0, min(255, tri.g))
                            tri.b = max(0, min(255, tri.b))
                    self.to_draw.append(tri)

        self.draw()




