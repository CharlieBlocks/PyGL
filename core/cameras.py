from .maths.array_operations import *
import math

class Camera:
    def __init__(self):
        self.pos = np.zeros(4)
        self.pos[3] = 1

        self.look_direction = np.zeros(4)
        self.look_direction[3] = 1

        self.vTarget = np.zeros(4)
        self.vTarget[3] = 1

        self.vUp = np.zeros(4)
        self.vUp[3] = 1

        self.fYaw = 0
        self.fAspectRatio = 0
        self.fFov = 0
        self.fNear = 0.3
        self.fFar = 1000

        self.camera_matrix = np.zeros((4,4))

    
    def create_matrix(self):
        self.vTarget[0] = 0
        self.vTarget[1] = 0
        self.vTarget[2] = 1

        matCameraRot = y_rotation_matrix(self.fYaw)
        self.look_direction = multiply_matrix(matCameraRot, self.vTarget)
        self.vTarget = vector_add(self.pos, self.look_direction)

        self.camera_matrix = matrix_pointAt(self.pos, self.vTarget, self.vUp)

        InvertMatrix(self.camera_matrix)

    def configure(self):
        self.vUp[1] = 1
        self.fFov = 90
        self.fAspectRatio = 1
        self.fFovRad = 1/math.tan(self.fFov * 0.5 / 180 * 3.14159)

