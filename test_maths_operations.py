import numpy as np
from core.maths import array_operations, vector_operations

print("Testing Vector Operations...")

vec = np.zeros((3,3), dtype=np.float32)

#Test scale_vector
vector_operations.scale_vector(vec, 10)

#Test translate_vector
vector_operations.translate_vector(vec, 1, 1, 1)

print("Vector operations complete")
print("Testing 2Darray_operations...")

vec = np.random.rand(3)
vec_2 = np.random.rand(3)

#Dot product
#_ = vector_operations.vector_dot_product(vec, vec_2)

#Cross_product
array_operations.cross_product(vec, vec_2)
#Normalise
array_operations.normalise_array(vec)

mat = np.random.rand(4,4)
array_operations.InvertMatrix(mat)

mat = np.zeros((4,4))
array_operations.create_rotation_matrix(mat, 300,10,45)


print("all array_operations working")