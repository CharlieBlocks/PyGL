import numba as nb
import numpy as np

@nb.njit
def scale_vector(arr, val):
    arr[0] *= val
    arr[1] *= val
    arr[2] *= val

@nb.vectorize(["float64(float64, float64)"], target='cuda')
def multiply_vector(arr, val):
    return arr * val

@nb.njit
def translate_vector(arr, x, y, z):
    arr[0] += x
    arr[1] += y
    arr[2] += z

@nb.njit
def vector_dot_product(arr_one, arr_two):
    dp = arr_one[0] * arr_two[0] + arr_one[1] * arr_two[1] + arr_one[2] * arr_two[2]
    return dp 

@nb.njit
def vector_subtract(vec1, vec2):
    out = np.zeros(4)
    out[3] = 1
    out[0] = vec1[0] - vec2[0]
    out[1] = vec1[1] - vec2[1]
    out[2] = vec1[2] - vec2[2]
    return out

@nb.vectorize(["float64(float64, float64)"], target='cuda')
def vector_add(vec1, vec2):
    return vec1 + vec2

    

        