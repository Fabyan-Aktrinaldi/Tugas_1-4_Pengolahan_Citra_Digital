### Matriks 3 Dimensi

import numpy as np

#### CARA CEPAT DENGAN Library Numpy ####

A = [ [[1, 2, 3],
       [4, 5, 6],
       [7, 8, 9]],

      [[11, 12, 13],
       [14, 15, 16],
       [17, 18, 19]]
    ]

B = [ [[1, 2, 3],
       [4, 5, 6],
       [7, 8, 9]],

      [[11, 12, 13],
       [14, 15, 16],
       [17, 18, 19]]
    ]

arr1 = np.array(A)
arr2 = np.array(B)

print("Matriks A:\n", arr1)
print("\nMatriks B:\n", arr2)

arrhasil = np.matmul(arr1, arr2)

C = arrhasil

print("\nMatriks Hasil Perkalian A x B:\n", C)




### CARA MANUAL TANPA LIBRARY ###

# A = [ [[1, 2, 3],
#        [4, 5, 6],
#        [7, 8, 9]],
#
#       [[11, 12, 13],
#        [14, 15, 16],
#        [17, 18, 19]]
#     ]
#
# B = [ [[1, 2, 3],
#        [4, 5, 6],
#        [7, 8, 9]],
#
#       [[11, 12, 13],
#        [14, 15, 16],
#        [17, 18, 19]]
#     ]
#
# C = [ [[0,0,0],
#        [0,0,0],
#        [0,0,0]],
#
#       [[0,0,0],
#        [0,0,0],
#        [0,0,0]]
#     ]
#
# N = 2
#
# for n in range(0,N):
#     for i in range(0,3):
#         for j in range(0,3):
#             for k in range(0,3):
#                 C[n][i][j] += A[n][i][k] * B[n][k][j]
#
# print("Matriks A:", A)
# print("Matriks B:", B)
#
# print("\nMatriks C:", C)
