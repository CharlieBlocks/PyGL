import numpy as np


class Triangle:
    def __init__(self):
        self.p = np.zeros((3,4))
        self.t = np.zeros((3,2))    
        self.normal = np.zeros(4)
        self.normal[3] = 1  

class Mesh:
    def __init__(self):
        self.m = []
        self.pos = np.array([0,0,0])
        self.rotation = np.zeros(3)
        self.scale = 1

        self.rot_mat = np.zeros((4,4))