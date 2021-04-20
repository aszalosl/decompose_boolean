"""Decompose heterogeneous matrices."""
from typing import List
from common import make_rows, coefficient_variant, move, join

global rows #: Dict[int,Set[int]]
global g


def attract(i:int, j:int) -> float:
    """
    Calculate the attraction between rows i and j.

    Parameters
    ----------
    i : the first row
    j : the second row

    Returns
    -------
    float: the force between rows.
    """
    global rows
    global columns
    global g
    if i==j:
        return 0.0
    else:
        s = coefficient_variant(rows[i]|set([i]), rows[j]|set([j]), columns[i]|set([i]), columns[j]|set([j]), g)
        # s = coefficient_variant(rows[i], rows[j], columns[i], columns[j], g)
    # different conversions:
    #return 3.125*s*s*s-7.5*s*s+6.375*s-1    # green
    #return 2* s**0.5-1                      # red
    #return -1.5*s*s + 3.5*s -1              # blue
    return s **(1./5.)*2-1                  # black
    #return 2*s-1                            # noname


def calc(matrix: List[List[int]]) -> List[List[int]]:
    """
    Biclustering.

    Parameters
    ----------
    m: homogeneous matrix of a relation

    Returns
    -------
    solution: "set of set of" objects, a clustering
    """
    global rows
    rows = make_rows(matrix)
    global columns
    columns = make_rows(list(map(list, zip(*matrix))))

    global g
    g = {x:x for x in range(len(rows))}
    change=False

    while True:
        change = False
        for i in g:
            if move(i,g,attract):
                change=True
        print("after move:", [list({i+1 for i in g if g[i]==v}) for v in set(g.values())])
        if join(g,attract):
            change=True
            print("after join:", [list({i+1 for i in g if g[i]==v}) for v in set(g.values())])
        if not change:
            break
    solution = [list({i+1 for i in g if g[i]==v}) for v in set(g.values())]
    return solution



if __name__ == "__main__":
    # example from Gunther Schmidt tech. rep. p12
    m = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 1
         [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 2
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 3
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 4
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],  # 5
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],  # 6
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 7
         [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 8
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 9
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 10
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 11
         [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 12
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  # 13
         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 14
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],  # 15
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 16
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 17
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 18
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]  # 19
    sol = calc(m)
    print(sol)
