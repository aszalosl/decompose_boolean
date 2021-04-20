"""Decomposing relations, p.13, tech. rep."""
# permutation
import decomp1
from printmatrix import txt

####  1  2  3  4  5  6  7
m = [[0, 0, 0, 1, 0, 0, 0],  # 1
     [0, 0, 1, 0, 0, 0, 0],  # 2
     [0, 0, 0, 0, 1, 0, 0],  # 3
     [0, 0, 0, 0, 0, 0, 1],  # 4
     [0, 0, 0, 0, 0, 1, 0],  # 5
     [0, 1, 0, 0, 0, 0, 0],  # 6
     [1, 0, 0, 0, 0, 0, 0]]  # 7
s=decomp1.calc(m)
print(s)
txt(s,s,m)
