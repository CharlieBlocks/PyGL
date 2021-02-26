import numpy as np
import math
import pygame
import os
import cupy as cp
from numpy.linalg import inv

class Scene:
    def __init__(self, screen, init_camera=True):
        self.screen = screen #The pygame screen to manipulate
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()

        self.objects = []

        self.camera = self.create_camera() if init_camera else None
        self.lights = []

        self.add_light()

    def create_camera(self):
        camera = Camera()
        camera.vUp.point[1] = 1
        camera.fFov = 90
        camera.fAspectRatio = self.WIDTH/self.HEIGHT
        camera.fFovRad = 1 / math.tan(camera.fFov * 0.5 / 180 * 3.14159)
        return camera    

    def add_light(self):
        light = Light()
        light.direction.point[2] = -1

        normalise_vector(light.direction)

        self.lights.append(light)

    def calculate_normals(self, mesh):
        for i in range(len(mesh.mesh)):
            tri = mesh.mesh[i]

            line1 = tri.p[1] - tri.p[0]
            line2 = tri.p[2] - tri.p[0]

            normal = vector_cross_product(line1, line2)

            normalise_vector(normal)

            mesh.mesh[i].normal = normal

    def add_triangle_from_array(self, array):
        vertex_1 = array[0]
        vertex_2 = array[1]
        vertex_3 = array[2]

        new_tri = Triangle()
        new_tri.p[0].point[0] = vertex_1[0]
        new_tri.p[0].point[1] = vertex_1[1]
        new_tri.p[0].point[2] = vertex_1[2]

        new_tri.p[1].point[0] = vertex_2[0]
        new_tri.p[1].point[1] = vertex_2[1]
        new_tri.p[1].point[2] = vertex_2[2]

        new_tri.p[2].point[0] = vertex_3[0]
        new_tri.p[2].point[1] = vertex_3[1]
        new_tri.p[2].point[2] = vertex_3[2]

        new_mesh = Mesh()
        new_mesh.mesh.append(new_tri)

        self.calculate_normals(new_mesh)

        self.objects.append(new_mesh)
        return new_mesh


    
    def load_obj(self, filename, textured): # A function that takes a path and refrence name then reads the obj file
        try:
            file_in = open(filename) #Read in file
        except:
            print("Could not open file") #Raise error if file could not be read
            raise

        filename, fileExtension = os.path.splitext(filename) #Check extension
        newObject = Mesh()  #Create the mesh and a pool of verticies
        vertex_pool = []

        textureUVs = []


        if not textured:
            for line in file_in:    #Read in file
                words = line.split()
                if words != []: #Get data and the begining letter
                    command = words[0]
                    data = words[1:]

                    if command == 'v':  #If command = v read in verticies and add to vertex pool
                        x,y,z = data 
                        vertex = Vector3()
                        vertex.point[0] = float(x) 
                        vertex.point[1] = float(y)
                        vertex.point[2] = float(z) 
                        vertex_pool.append(vertex)

                    if command == 'f':  #If command = f create a triangle using specified verticies
                        for word in data:
                            vi = data[0]
                            ti = data[1]
                            ni = data[2]

                            indices = (int(vi) -1, int(ti) - 1, int(ni) - 1)
                            newTri = Triangle()
                            newTri.p[0] = vertex_pool[indices[0]]
                            newTri.p[1] = vertex_pool[indices[1]]
                            newTri.p[2] = vertex_pool[indices[2]]

                            newObject.mesh.append(newTri)
            
            newObject.r = 255   #Give a defualt colour
            newObject.g = 255
            newObject.b = 255

            self.calculate_normals(newObject) #Calculate the normals

            self.objects.append(newObject) #Add object
            return newObject

        if textured:
            for line in file_in:    #Read in file
                words = line.split()
                if words != []: #Get data and the begining letter
                    command = words[0]
                    data = words[1:]

                    if command == 'v':  #If command = v read in verticies and add to vertex pool
                        x,y,z = data 
                        vertex = Vector3()
                        vertex.point[0] = x 
                        vertex.point[1] = y 
                        vertex.point[2] = z 
                        vertex_pool.append(vertex)

                    if command == 'vt':
                        u, v = data 
                        tex = Vector2()
                        tex.u = u 
                        tex.v = v 
                        textureUVs.append(tex)

                    if command == 'f':  #If command = f create a triangle using specified verticies
                        vertices = []
                        UVs = []
                        for word in data:

                            for v in data:
                                to_seperate = list(v)
                                vertex_indice = []
                                UV_indice = []
                                change = False
                                for n in to_seperate:
                                    if n != "/":
                                        if change == False:
                                            vertex_indice.append(n)
                                        else:
                                            UV_indice.append(n)
                                    else:
                                        change = True

                                UV = "".join(UV_indice)
                                Vertex = "".join(vertex_indice)
                                vertices.append(Vertex)
                                UVs.append(UV)
                            
                            vi = vertices[0]
                            ti = vertices[1]
                            ni = vertices[2]

                            at = UVs[0]
                            bt = UVs[1]
                            ct = UVs[2]

                            
                            indices = (int(vi) -1, int(ti) - 1, int(ni) - 1)
                            tex_indices = (int(at) - 1, int(bt) - 1, int(ct) - 1)
                            newTri = Triangle()
                            newTri.p[0] = vertex_pool[indices[0]]
                            newTri.p[1] = vertex_pool[indices[1]]
                            newTri.p[2] = vertex_pool[indices[2]]
                            newTri.t[0] = textureUVs[tex_indices[0]]
                            newTri.t[1] = textureUVs[tex_indices[1]]
                            newTri.t[2] = textureUVs[tex_indices[2]]

                            newObject.mesh.append(newTri)
                            

                    if command == 'vt':
                        u, v = data 
                        texCord = Vector2()
                        texCord.u = u 
                        texCord.v = v
            

            self.calculate_normals(newObject) #Calculate the normals

            self.objects.append(newObject) #Add object
            return newObject


    def update(self, renderer):
        renderer.render(self.objects, self.camera, self.lights)



class Basic_Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.projection_matrix = Matrix4x4()
        self.last_camera_pos = 0
        self.last_camera_lookDirection = 0
        self.last_camera_fov = 0

        self.camera_matrix = 0

        self._init = False
        self.threads = 2
    
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
            
          #  print((tri.p[0].point[0], tri.p[0].point[1]), (tri.p[1].point[0], tri.p[1].point[1]), (tri.p[2].point[0], tri.p[2].point[1]))
            pygame.draw.polygon(self.screen, colour, ((tri.p[0].point[0], tri.p[0].point[1]), (tri.p[1].point[0], tri.p[1].point[1]), (tri.p[2].point[0], tri.p[2].point[1])))
        pygame.display.flip()

        

    def render(self, objects, camera, lights):
        self.to_draw = []
        #Only update camera transforms if the camera state has changed
        if self.last_camera_pos != camera.pos or self.last_camera_lookDirection != camera.look_direction or not self._init:

            camera.vTarget.point[0] = 0
            camera.vTarget.point[1] = 0
            camera.vTarget.point[2] = 1


            matCameraRot = matrix_rotationY(camera.fYaw)
            camera.look_direction = matCameraRot * camera.vTarget
            camera.vTarget = camera.pos + camera.look_direction
            
            self.camera_matrix = Matrix4x4()
            self.camera_matrix = matrix_pointAt(camera.pos, camera.vTarget, camera.vUp)
            
            self.camera_matrix = Invert(self.camera_matrix)

            self._init = True
        
            self.last_camera_pos = camera.pos 
            self.last_camera_lookDirection = camera.look_direction

        #threads = []
        for j in objects:
            for i in j.mesh:
                #process = Thread(target=self.render_triangle, args=[i, j, lights])
                #process.start()
                #threads.append(process)

        #for process in threads:
            #process.join()
                
                tri = transplant_vector(i)
                normal = tri.normal

                #Apply camera transform
                tri.p[0] = self.camera_matrix * tri.p[0]
                tri.p[1] = self.camera_matrix * tri.p[1]
                tri.p[2] = self.camera_matrix * tri.p[2]

                
                x_rotation = matrix_rotationX(j.rot[0])
                y_rotation = matrix_rotationY(j.rot[1])
                z_rotation = matrix_rotationZ(j.rot[2])

                tri.p[0] = x_rotation * tri.p[0]
                tri.p[1] = x_rotation * tri.p[1]
                tri.p[2] = x_rotation * tri.p[2]
                normal = x_rotation * normal
                

                tri.p[0] = y_rotation * tri.p[0]
                tri.p[1] = y_rotation * tri.p[1]
                tri.p[2] = y_rotation * tri.p[2]
                normal = y_rotation * normal


                tri.p[0] = z_rotation * tri.p[0]
                tri.p[1] = z_rotation * tri.p[1]
                tri.p[2] = z_rotation * tri.p[2]
                normal = z_rotation * normal

                if normal.point[2] < 0:
                    scale_triangle(tri, j.pos.point[2] + j.scale)
                    translate_triangle(tri, j.pos.point[0], j.pos.point[1])

                    for light in lights:
                        dp = normal.point[0] * light.direction.point[0] + normal.point[1] * light.direction.point[1] + normal.point[2] * light.direction.point[2]

                        light_r = min(255, tri.r*dp)#
                        light_g = min(255, tri.g*dp)
                        light_b = min(255, tri.b*dp)
                        
                        tri.r = abs(light_r)
                        tri.g = abs(light_g)
                        tri.b = abs(light_b)

                        tri.r = max(0, min(255, tri.r))
                        tri.g = max(0, min(255, tri.g))
                        tri.b = max(0, min(255, tri.b))

                    self.to_draw.append(tri)
        self.draw()



                


## Helper Functions ##
def scale_triangle(in_tri, scale):
    in_tri.p[0].point[0] *= scale
    in_tri.p[0].point[1] *= scale

    in_tri.p[1].point[0] *= scale
    in_tri.p[1].point[1] *= scale

    in_tri.p[2].point[0] *= scale
    in_tri.p[2].point[1] *= scale

def translate_triangle(in_tri, x, y):
    in_tri.p[0].point[0] += x
    in_tri.p[0].point[1] += y

    in_tri.p[1].point[0] += x
    in_tri.p[1].point[1] += y

    in_tri.p[2].point[0] += x
    in_tri.p[2].point[1] += y

def transplant_vector(in_tri):
    new_tri = Triangle()
    new_tri.p[0].point[0] = in_tri.p[0].point[0]
    new_tri.p[0].point[1] = in_tri.p[0].point[1]
    new_tri.p[0].point[2] = in_tri.p[0].point[2]

    new_tri.p[1].point[0] = in_tri.p[1].point[0]
    new_tri.p[1].point[1] = in_tri.p[1].point[1]
    new_tri.p[1].point[2] = in_tri.p[1].point[2]

    new_tri.p[2].point[0] = in_tri.p[2].point[0]
    new_tri.p[2].point[1] = in_tri.p[2].point[1]
    new_tri.p[2].point[2] = in_tri.p[2].point[2]

    new_tri.normal = in_tri.normal

    new_tri.t[0] = in_tri.t[0]
    new_tri.t[1] = in_tri.t[1]
    new_tri.t[2] = in_tri.t[2]

    return new_tri

def vector_dot_product(VectorOne, VectorTwo):
    dp = VectorOne.point[0] * VectorTwo.point[0] + VectorOne.point[1] * VectorTwo.point[1] + VectorOne.point[2] * VectorTwo.point[2]
    return dp

def normalise_vector(vector):
    l = math.sqrt(vector.point[0]*vector.point[0] + vector.point[1]*vector.point[1] + vector.point[2]*vector.point[2])
    vector.point[0] = vector.point[0] / l if l != 0 else 0 
    vector.point[1] = vector.point[1] / l if l != 0 else 0
    vector.point[2] = vector.point[2] / l if l != 0 else 0

def vector_cross_product(vector_one, vector_two):
    out = Vector3()
    out.point[0] = vector_one.point[1] * vector_two.point[2] - vector_one.point[2] * vector_two.point[1]
    out.point[1] = vector_one.point[2] * vector_two.point[0] - vector_one.point[0] * vector_two.point[2]
    out.point[2] = vector_one.point[0] * vector_two.point[1] - vector_one.point[1] * vector_two.point[0]
    return out

def matrix_pointAt(pos, target, up):
     # Callculate new forward direction
    newForward = Vector3()
    newForward = target - pos
    normalise_vector(newForward)

    #Calculate new up relation
    a = multiply_vector(newForward, vector_dot_product(up, newForward))

    newUp = up - a
    normalise_vector(newUp)

    #New Right Direction (cross Product)
    newRight = vector_cross_product(newUp, newForward)

    matrix = Matrix4x4()
    matrix.m[0][0] = newRight.point[0]
    matrix.m[0][1] = newRight.point[1]
    matrix.m[0][2] = newRight.point[2]
    matrix.m[0][3] = 0 

    matrix.m[1][0] = newUp.point[0]
    matrix.m[1][1] = newUp.point[1]
    matrix.m[1][2] = newUp.point[2]
    matrix.m[1][3] = 0

    matrix.m[2][0] = newForward.point[0]
    matrix.m[2][1] = newForward.point[1]
    matrix.m[2][2] = newForward.point[2]
    matrix.m[2][3] = 0

    matrix.m[3][0] = pos.point[0]
    matrix.m[3][1] = pos.point[1]
    matrix.m[3][2] = pos.point[2]
    matrix.m[3][3] = 1

    return matrix



def matrix_rotationX(fAngle):
    
    sin = math.sin(fAngle*0.01745)
    cos = math.cos(fAngle*0.01745)

    #Create rotation matrix for Z axis
    RotationMatrixX = Matrix4x4()
    
    RotationMatrixX.m[0][0] = 1
    RotationMatrixX.m[1][1] = cos
    RotationMatrixX.m[1][2] = sin
    RotationMatrixX.m[2][1] = -sin
    RotationMatrixX.m[2][2] = cos
    RotationMatrixX.m[3][3] = 1
    
    
    return RotationMatrixX
    

def matrix_rotationY(fAngle):

    sin = math.sin(fAngle*0.01745)
    cos = math.cos(fAngle*0.01745)
    
    matrix = Matrix4x4()
    
    matrix.m[0][0] = cos
    matrix.m[0][2] = sin
    matrix.m[2][0] = -sin
    matrix.m[1][1] = 1
    matrix.m[2][2] = cos
    matrix.m[3][3] = 1
    
    
    return matrix
    

def matrix_rotationZ(fAngle):

    sin = math.sin(fAngle*0.01745)
    cos = math.cos(fAngle*0.01745)

    RotationMatrixZ = Matrix4x4()
    
    RotationMatrixZ.m[0][0] = cos
    RotationMatrixZ.m[0][1] = sin
    RotationMatrixZ.m[1][0] = -sin
    RotationMatrixZ.m[1][1] = cos
    RotationMatrixZ.m[2][2] = 1
    RotationMatrixZ.m[3][3] = 1
    

    return RotationMatrixZ
    



def multiply_vector(vector, Float):
    out = Vector3()

    out.point[0] = vector.point[0] * Float
    out.point[1] = vector.point[1] * Float
    out.point[2] = vector.point[2] * Float

    return out      

def Invert(mat):
    OutputMatrix = Matrix4x4()
    OutputMatrix.m = inv(mat.m)
    return OutputMatrix

############# Structures Classes ################

class Vector3():
    def __init__(self):
        self.point = np.zeros(4)
        self.point[3] = 1

    def __add__(self, other):
        out = Vector3()
        out.point[0] = self.point[0] + other.point[0]
        out.point[1] = self.point[1] + other.point[1] 
        out.point[2] = self.point[2] + other.point[2]
        return out

    def __sub__(self, other):
        out = Vector3()
        out.point[0] = self.point[0] - other.point[0]
        out.point[1] = self.point[1] - other.point[1]
        out.point[2] = self.point[2] - other.point[2]
        return out
         

class Vector2():
    def __init__(self):
        self.u = 0
        self.v = 0
        self.w = 1

class Triangle():
    def __init__(self):
        self.p = [Vector3(), Vector3(), Vector3()]
        self.t = [Vector2(), Vector2(), Vector2()]
        self.normal = 0

        self.r = 255 
        self.g = 255
        self.b = 255

class Mesh():
    def __init__(self):
        self.mesh = []
        self.origin = Vector3()
        
        self.rot = [0,0,0]
        self.pos = Vector3()
        self.scale = 1

        self.visible = True

class Matrix4x4():
    def __init__(self):
        self.m = np.zeros((4, 4))

    def __mul__(self, i):
        v = Vector3()
        v.point = i.point.dot(self.m)
        return v
        
        """
        v = Vector3()
        v.x = float(i.x) * self.m[0][0] + float(i.y) * self.m[1][0] + float(i.z) * self.m[2][0] + float(i.w) * self.m[3][0]
        v.y = float(i.x) * self.m[0][1] + float(i.y) * self.m[1][1] + float(i.z) * self.m[2][1] + float(i.w) * self.m[3][1]
        v.z = float(i.x) * self.m[0][2] + float(i.y) * self.m[1][2] + float(i.z) * self.m[2][2] + float(i.w) * self.m[3][2]
        v.w = float(i.x) * self.m[0][3] + float(i.y) * self.m[1][3] + float(i.z) * self.m[2][3] + float(i.w) * self.m[3][3]

        if i.w != 0:
            v.x /= i.w 
            v.y /= i.w 
            v.z /= i.w 

        return v
        """

class Camera():
    def __init__(self):
        self.pos = Vector3()
        self.look_direction = Vector3()
        self.vTarget = Vector3()
        self.vUp = Vector3()
        self.fYaw = 0
        self.fAspectRatio = 0
        self.fFov = 0
        self.fFovRad = 0
        self.fNear = 0.3
        self.fFar = 1000

class Light():
    def __init__(self):
        self.pos = Vector3()
        self.direction = Vector3()


