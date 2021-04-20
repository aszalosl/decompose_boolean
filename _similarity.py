#%% similarity coefficients

from typing import List,Set
import random

def jaccard(s1:Set[int],s2:Set[int]) -> float:
    """
    Jaccard similarity.

    Parameters
    ----------
    s1 : first set.
    s2 : second set.

    Returns
    -------
    similarity coefficient (0<=x<=1).
    """
    if len(s1|s2)==0:
        return 0.0
    else:
        return len(s1&s2)/len(s1|s2)

def overlap(s1:Set[int],s2:Set[int]) -> float:
    """
    Overlap similarity.

    Parameters
    ----------
    s1 : first set.
    s2 : second set.

    Returns
    -------
    similarity coefficient (0<=x<=1).
    """
    return len(s1&s2)/min(len(s1),len(s2))

def sorensen(s1,s2) -> float:
    """
    Sorensen similarity.

    Parameters
    ----------
    s1 : first set.
    s2 : second set.

    Returns
    -------
    similarity coefficient (0<=x<=1).
    """
    return 2*len(s1&s2)/(len(s1)+len(s2))

#%% generate a random matrix
def random_matrix(a:int,b:int) -> List[List[int]]:
    """
    Generate a random boolean matrix, each row and each column contains 1 somewhere.

    Parameters
    ----------
    a : number of rows.
    b : number of columns.

    Returns
    -------
    m : a random matrix of size axb
    """
    br=list(range(b))
    random.shuffle(br)
    # empty matrix
    mm = [[0 for _ in range(b)] for _ in range(a)]
    # for each row
    for i in range(a):
        mm[i][br[i]]=1
    # for each column
    for j in range(b):
        mm[random.randrange(a)][j]=1
    return mm
