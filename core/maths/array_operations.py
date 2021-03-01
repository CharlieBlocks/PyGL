import numba as nb #To speed up operations
import cupy as cp
import numpy as np
from .vector_operations import *

def normalise_array(arr):
    l = np.sqrt(arr[0]*arr[0] + arr[1]*arr[1] + arr[2]*arr[2])
    if l != 0:
        arr[0] /= l 
        arr[1] /= l 
        arr[2] /= l 
    else:
        return 


def cross_product(arr_one, arr_two): #Must be a 1D array of 3
    out = np.zeros(4)
    out[0] = arr_one[1] * arr_two[2] - arr_one[2] * arr_two[1]
    out[1] = arr_one[2] * arr_two[0] - arr_one[0] * arr_two[2]
    out[2] = arr_one[0] * arr_two[1] - arr_one[1] * arr_two[0]
    out[3] = 1
    return out

@nb.njit
def InvertMatrix(mat):
    mat = np.linalg.inv(mat)

@nb.njit
def y_rotation_matrix(fAngle):
    mat = np.zeros((4,4))
    sin = np.sin(fAngle*0.01745)
    cos = np.cos(fAngle*0.01745)

    mat[0][0] = cos
    mat[0][2] = sin
    mat[2][0] = -sin
    mat[1][1] = 1
    mat[2][2] = cos
    mat[3][3] = 1

    return mat

@nb.njit
def multiply_matrix(mat, vec):
    return np.dot(mat, vec)

@nb.njit
def create_rotation_matrix(x, y, z):

    mat_x = np.zeros((4,4))
    mat_y = np.zeros((4,4))
    mat_z = np.zeros((4,4))

    sin_x = np.sin(x*0.01745)    #Precalculate the sines and cosines
    cos_x = np.cos(x*0.01745)    #This halfs the amount of caluclations to be done

    sin_y = np.sin(y*0.01745)
    cos_y = np.cos(y*0.01745)

    sin_z = np.sin(z*0.01745)
    cos_z = np.cos(z*0.01745)

    mat_x[0][0] = 1   #Set the X matrix.
    mat_x[1][1] += cos_x
    mat_x[1][2] += sin_x
    mat_x[2][1] += -sin_x
    mat_x[2][2] += cos_x
    mat_x[3][3] = 1 

    mat_y[0][0] = cos_y
    mat_y[0][2] = sin_y
    mat_y[2][0] = -sin_y
    mat_y[1][1] = 1
    mat_y[2][2] = cos_y
    mat_y[3][3] = 1

    mat_z[0][0] = cos_z
    mat_z[0][1] = sin_z
    mat_z[1][0] = -sin_z
    mat_z[1][1] = cos_z
    mat_z[2][2] = 1
    mat_z[3][3] = 1

    mat = np.dot(mat_x, mat_y)
    mat = np.dot(mat, mat_z)

    return mat


def matrix_pointAt(pos, target, up):
    new_forward = np.zeros(3)
    new_forward = vector_subtract(target, pos)
    a = multiply_vector(new_forward, vector_dot_product(up, new_forward))

    newUp = vector_subtract(up, a)
    normalise_array(newUp)

    newRight = cross_product(newUp, new_forward)

    matrix = np.zeros((4,4))
    matrix[0][0] = newRight[0]
    matrix[0][1] = newRight[1]
    matrix[0][2] = newRight[2]
    matrix[0][3] = 0 

    matrix[1][0] = newUp[0]
    matrix[1][1] = newUp[1]
    matrix[1][2] = newUp[2]
    matrix[1][3] = 0

    matrix[2][0] = new_forward[0]
    matrix[2][1] = new_forward[1]
    matrix[2][2] = new_forward[2]
    matrix[2][3] = 0

    matrix[3][0] = pos[0]
    matrix[3][1] = pos[1]
    matrix[3][2] = pos[2]
    matrix[3][3] = 1

    return matrix

