import numba as nb

@nb.guvectorize([(nb.float64[:], nb.float64[:], nb.float64[:])], '(n),(n)->(n)', target='cuda')
def multiply_matrix_vectorized(mat, tri, out):
    out[0] = tri[0] * mat[0] + tri[1] * mat[4] + tri[2] * mat[8] + tri[3] * mat[12]
    out[1] = tri[0] * mat[1] + tri[1] * mat[5] + tri[2] * mat[9] + tri[3] * mat[13]
    out[2] = tri[0] * mat[2] + tri[1] * mat[6] + tri[2] * mat[10] + tri[3] * mat[14]
    out[3] = tri[0] * mat[3] + tri[1] * mat[7] + tri[2] * mat[11] + tri[3] * mat[15]

@nb.guvectorize([(nb.float64[:], nb.float64[:], nb.float64[:])], '(n),()->(n)', target='cuda')
def scale_vector_vectorized(tri, scale, out):
    out[0] = tri[0] * scale[0] 
    out[1] = tri[1] * scale[0]
    out[2] = tri[2] * scale[0]
    out[3] = 1

@nb.guvectorize([(nb.float64[:], nb.float64[:], nb.float64[:], nb.float64[:], nb.float64[:])], '(n),(n),(n),(n)->(n)', target='cuda')
def translate_vector_vectorized(tri, x, y, z, out):
    out[0] = tri[0] + x[0] 
    out[1] = tri[1] + y[0]
    out[2] = tri[2] + z[0]
    out[3] = 1

@nb.guvectorize([(nb.float64[:], nb.float64[:], nb.float64[:])], '(),()->()', target='cuda')
def vector_dot_product_vectorized(arr_one, arr_two, out):
    out[0] = arr_one[0] * arr_two[0] + arr_one[1] * arr_two[1] + arr_one[2] * arr_two[2]