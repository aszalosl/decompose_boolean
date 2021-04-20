"""Calculate the decomposition of heterogeneous boolean matrices."""
#import operator
from typing import Dict,List,Set,Tuple
from common import make_rows, coefficient, move, join


ga:Dict[int,int]={}  # clustering of rows
gb:Dict[int,int]={}  # clustering of columns
fa:Dict[Tuple[int,int],float] # forces between rows
fb:Dict[Tuple[int,int],float] # forces between columns

#%% utility functions

#from math import sqrt
def calc(al0:Dict[int,Set[int]], g:Dict[int,int]) -> Dict[Tuple[int,int], float]:
    """
    Precalculate the forces between rows/columns.

    Parameters
    ----------
    al0 : rows/columns and their content.
    g : clustering of columns/rows.

    Returns
    -------
    dict of forces, 0<=fxy<=1.

    """
    d : Dict[Tuple[int,int], float] = {}

    for k1 in al0:
        for k2 in al0:
            if k1==k2:
                d[k1,k2]=0.0
            elif k1<k2:
                v = coefficient(al0[k1], al0[k2], g)
                if v>0:
                    #vv = 3.125*v*v*v-7.5*v*v+6.375*v-1  # green
                    #vv = 2*sqrt(v)-1                   # red
                    #vv = -1.5*v*v + 3.5*v -1           # blue
                    vv = v **(1./5.)*2-1               # black
                    #vv = 2*v-1                         # noname
                    #vv = 2*v*v*v-1                     # for Ferrer
                    d[k1,k2]=vv
                    d[k2,k1]=vv
    return d


def attract_rows(i: int, j:int) -> float:
    """
    Retrieve the force between rows i and j.

    Parameters
    ----------
    i : first row.
    j : second row.

    Returns
    -------
    float : the force  -1<=f<=1
    """
    global fa
    return fa.get((i,j),-1.0)

def attract_columns(i: int, j:int) -> float:
    """
    Retrieve the force between columns i and j.

    Parameters
    ----------
    i : first column.
    j : second column.

    Returns
    -------
    float : the force  -1<=f<=1
    """
    global fb
    return fb.get((i,j),-1.0)


#%% correlation clustering.


def bi_corr_clustering(a_list:Dict[int,Set[int]], b_list:Dict[int,Set[int]]) -> None:
    """
    Two 'parallel' clustering.

    Parameters
    ----------
    a_list : the rows.
    b_list : the columns.

    Returns
    -------
    None, the result of the clustering is in variables ga and gb.
    """
    global ga
    global gb
    global fa
    global fb
    ga={x:x for x in range(len(a_list))}
    gb={x:x for x in range(len(b_list))}
    changeA,changeB=False,False
    while True:
        any_change=False
        fa = calc(a_list, gb)
        while True:
            changeA = False
            for i in ga:
                if move(i,ga,attract_rows):
                    changeA=True
                    any_change=True
            if join(ga,attract_rows):
                changeA=True
                any_change=True
            if not changeA:
                break
        #print("GA:",[list({i+1 for i in ga if ga[i]==v}) for v in set(ga.values())])
        fb = calc(b_list, ga)
        while True:
            changeB = False
            for i in gb:
                if move(i,gb,attract_columns):
                    changeB=True
                    any_change=True
            if join(gb,attract_columns):
                changeB=True
                any_change=True
            if not changeB:
                break
        #print("GB:",[list({i+1 for i in gb if gb[i]==v}) for v in set(gb.values())])
        if not any_change:
            break


def start(matrix: List[List[int]]) -> Tuple[List[List[int]],List[List[int]]]:
    """
    Determine the decomposition of the matrix.

    Parameters
    ----------
    matrix : the input

    Returns
    -------
    Clustering of rows and the columns.
    """
    list1=make_rows(matrix) # break up the matrix into rows
    transposed :List[List[int]] = [list(x) for x in zip(*matrix)]
    list2=make_rows(transposed) # break up the matrix into columns (the rows of its transpose)
    bi_corr_clustering(list1,list2)
    solution1 = [list({i+1 for i in ga if ga[i]==v}) for v in set(ga.values())]
    solution2 = [list({i+1 for i in gb if gb[i]==v}) for v in set(gb.values())]

    return solution1,solution2


if __name__ == "__main__":
    #      1 2 3 4 5 6 7 8 9 0 1 2 3
    m  = [[0,0,0,0,0,1,0,0,0,0,0,0,0],   # 1
          [0,0,0,1,0,0,0,0,0,0,0,0,0],   # 2
          [1,0,0,0,0,0,0,1,0,0,0,0,0],   # 3
          [0,0,0,0,1,0,0,0,0,1,0,0,0],   # 4
          [0,0,0,0,0,0,0,0,0,0,0,0,0],   # 5
          [1,0,0,0,0,0,0,1,0,0,0,0,0],   # 6
          [0,0,0,1,0,0,0,1,0,0,0,0,0],   # 7
          [0,0,0,0,0,0,0,0,0,0,0,0,0],   # 8
          [0,0,1,0,0,1,0,0,0,0,0,0,0],   # 9
          [0,0,0,0,0,0,0,0,0,0,0,0,0],   # 0
          [0,0,0,0,0,1,1,0,0,0,0,0,0],   # 1
          [0,0,0,0,0,0,0,0,0,0,0,0,0],   # 2
          [0,0,0,0,1,0,0,0,1,0,0,0,0],   # 3
          [0,1,0,0,0,0,0,0,0,1,0,0,0],   # 4
          [0,0,0,0,0,0,1,0,0,0,0,0,1],   # 5
          [0,0,1,0,0,0,0,0,0,0,0,0,1],   # 6
          [0,0,0,0,0,1,0,0,0,0,0,0,0]]   # 7

    g1,g2=start(m)
    print(g1,g2)

