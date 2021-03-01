import copy
from ..maths import *
import pygame
import time

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

    def draw(self, tris, rgbs):
        self.screen.fill("black")
        #pygame.display.flip()
        """
        for tri in self.to_draw:
            RGB = (int(tri.r), int(tri.g), int(tri.b))

            colour = self._from_rgb(RGB)
        """
        for num, tri in enumerate(tris):
            rgb = rgbs[num]
            pygame.draw.polygon(self.screen, self._from_rgb(rgb), ((tri[0][0], tri[0][1]), (tri[1][0], tri[1][1]), (tri[2][0], tri[2][1])))
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

            j.rot_mat = create_rotation_matrix(j.rotation[0], j.rotation[1], j.rotation[2])

            cam_mat = [] #Prepeares the triangles and camera matrix for vectorized multiplication
            normals = []
            tris = []
            rot_mat = []
            for x in range(len(j.m)):
                tris.append(j.m[x].p)
                normals.append(j.m[x].normal)
                cam_mat.append(camera.camera_matrix)
                cam_mat.append(camera.camera_matrix)
                cam_mat.append(camera.camera_matrix)
                rot_mat.append(j.rot_mat)
                rot_mat.append(j.rot_mat)
                rot_mat.append(j.rot_mat)


            tris = np.array(tris)
            cam_mat = np.array(cam_mat)
            rot_mat = np.array(rot_mat)
            normals = np.array(normals)

            tris = tris.reshape(-1,4)
            tris = np.pad(tris, [(0,0), (0,12)]) #Pad the array to work with the vectorized multiplication function
            cam_mat = cam_mat.reshape(-1,16)
            rot_mat = rot_mat.reshape(-1, 16)
            normals = normals.reshape(-1,4)
            normals = np.pad(normals, [(0,0), (0,12)])

            tris = multiply_matrix_vectorized(cam_mat, tris) #Multiplication for camera_matrix
            tris = multiply_matrix_vectorized(rot_mat, tris) # multiplication for rotation_matrix
            rot_mat = rot_mat[:normals.shape[0]]
            normals = multiply_matrix_vectorized(rot_mat, normals)
            tris = tris[0:tris.shape[0], :4]
            tris = tris.reshape(-1,3,4) #Rehsape and remove excess padding
            normals = normals[0:normals.shape[0], :4]
            normals = normals.reshape(-1,4)

            new_tris = tris 
            new_normals = normals
            num = normals.shape[0]
            while num >0:
                tri = tris[num-1]
                normal = normals[num-1]
                if normal[2] >= 0:
                    new_tris = np.delete(new_tris, num-1, 0)
                    new_normals = np.delete(new_normals, num-1, 0)
                num -= 1

            tris = new_tris 
            normals = new_normals
            tris = tris.reshape(-1, 4)
            
            proj_mat = []
            for index in range(tris.shape[0]):
                proj_mat.append(self.projection_matrix)

            scale = np.full(tris.shape[0], j.scale, dtype=np.float64)
            x = np.full(tris.shape, j.pos[0], dtype=np.float64)
            y = np.full(tris.shape, j.pos[1], dtype=np.float64)
            z = np.full(tris.shape, j.pos[2], dtype=np.float64)

            proj_mat = np.array(proj_mat)
            proj_mat = proj_mat.reshape(-1, 16)
            tris = np.ascontiguousarray(tris, dtype=np.float64)

            tris = scale_vector_vectorized(tris, scale) #Scale triangle

            tris = translate_vector_vectorized(tris,x,y,z)

            tris = np.pad(tris, [(0,0), (0,12)])
            tris = multiply_matrix_vectorized(proj_mat, tris)   
            tris = tris[0:tris.shape[0], :4]  
            tris = tris.reshape(-1,3,4)   


            for light in lights:
                if not light.custom_script:
                    light_normal = []
                    for index in range(normals.shape[0]):
                        light_normal.append(light.normal)
                    
                    light_normal = np.array(light_normal).reshape(-1, 4)
                    normals = np.ascontiguousarray(normals)

                    dp = vector_dot_product_vectorized(normals, light_normal)
                    
                    rgbs = []
                    for num, tri in enumerate(tris):
                        r = abs(min(255, self.colour[0]*dp[num][0]))
                        g = abs(min(255, self.colour[1]*dp[num][0]))
                        b = abs(min(255, self.colour[2]*dp[num][0]))

                        r = max(0, min(255, r))
                        g = max(0, min(255, g))
                        b = max(0, min(255, b))
                        rgb = (int(r),int(g),int(b))
                        rgbs.append(rgb)

        self.draw(tris, rgbs)




