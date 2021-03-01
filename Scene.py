#Import libarys
from .core.maths import *
from .core.Structures import *
import numpy as np
import os
import numpy as np


class Scene:
    def __init__(self, window_size):
        self.height = window_size[0]
        self.width = window_size[1]
        self.objects = []

    def calculate_normals(self, mesh):
        for i in mesh.m:

            line1 = vector_subtract(i.p[1], i.p[0])
            line2 = vector_subtract(i.p[2], i.p[0])

            normal = cross_product(line1, line2)
            normalise_array(normal)
            i.normal = normal

    def load_obj(self, filename): # A function that takes a path and refrence name then reads the obj file
        try:
            file_in = open(filename) #Read in file
        except:
            print("Could not open file") #Raise error if file could not be read
            raise

        filename, fileExtension = os.path.splitext(filename) #Check extension
        newObject = Mesh()  #Create the mesh and a pool of verticies
        vertex_pool = []

        textureUVs = []


        for line in file_in:    #Read in file
            words = line.split()
            if words != []: #Get data and the begining letter
                command = words[0]
                data = words[1:]

                if command == 'v':  #If command = v read in verticies and add to vertex pool
                    x,y,z = data 
                    vertex = [0,0,0,1]
                    vertex[0] = float(x) 
                    vertex[1] = float(y)
                    vertex[2] = float(z) 
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

                    newObject.m.append(newTri)

        self.calculate_normals(newObject) #Calculate the normals
        newObject.m = np.array(newObject.m)

        self.objects.append(newObject) #Add object
        return newObject