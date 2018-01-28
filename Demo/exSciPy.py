from scipy import sparse
import numpy as np
eye = np.eye(4)
print("NumPy array:\n{}".format(eye))
sparse_matrix = sparse.csr_matrix(eye)
print("\n{}".format(sparse_matrix))