# -*- coding: utf-8 -*-
"""Common routines for decomposition."""
import random
from typing import Dict,List,Set,Tuple,Callable


def make_rows(matrix: List[List[int]]) -> Dict[int,Set[int]]:
    """
    Break a matrix into rows, where rows are set of indices.

    Parameters
    ----------
    matrix : a boolean matrix

    Returns
    -------
    d : an associative array of row_ids and set of column_ids.
    """
    d = {}
    for i,line in enumerate(matrix):
        d[i] = set([j for j,l in enumerate(line) if l])
    return d


def _upper_appr(s:Set[int], g:Dict[int,int]) -> Set[int]:
    """
    Upper approximation of the set S.

    Parameters
    ----------
    s : a set of rows/columns.
    g : clustering of rows/columns.

    Returns
    -------
    The upper approximation - a set again.
    """
    t = {g[x] for x in s}  # the concerned clusters
    return {x for x in g if g[x] in t}  # we need to sum the size of the clusters


def coefficient(s1:Set[int],s2:Set[int], g:Dict[int,int]) -> float:
    """
    Variant of the Jaccard similarity coefficient.

    Parameters
    ----------
    s1 : first set of columns/rows
    s2 : second set of columns/rows
    g  : the corresponding clustering of columns/rows
    Returns
    -------
    similarity measure (0<=x<=1).
    """
    u1=_upper_appr(s1, g)
    u2=_upper_appr(s2, g)
    if len(u1|u2)==0:  # special case, or we can say that if both of them are empty, they are similar
        return 1.0
    else:
        return len(u1&u2)/len(u1|u2)

def coefficient_variant(s1:Set[int],s2:Set[int], s3:Set[int],s4:Set[int], g:Dict[int,int]) -> float:
    """
    Variant of the Jaccard similarity coefficient.

    Parameters
    ----------
    s1 : first set of columns/rows
    s2 : second set of columns/rows
    g  : the corresponding clustering of columns/rows
    Returns
    -------
    similarity measure (0<=x<=1).
    """
    u1=_upper_appr(s1, g)
    u2=_upper_appr(s2, g)
    u3=_upper_appr(s3, g)
    u4=_upper_appr(s4, g)
    if len(u1|u2)+len(u3|u4)==0:  # special case, or we can say that if both of them are empty, they are similar
        return 1.0
    else:
        return len((u1&u2)|(u3&u4))/(len(u1|u2)+len(u3|u4))


def move(i:int, g:Dict[int,int], f:Callable[[int,int],float]) -> bool:
    """
    Move object i to the most attractive cluster.

    Parameters
    ----------
    i : id of the object
    g : clustering of
    f : function to calculate forces between objects.

    Returns
    -------
    bool Has changed something? If yes, then g has modified.
    """
    fm:Dict[int,float] = {}     # superposition of forces by cluster
    for k in g:                 # take all the objects
        fm[g[k]]=fm.get(g[k],0.0)+f(i,k)
    fm_max=max(fm.values())     # take the most attractive force
    if fm_max>0 and fm_max>fm.get(g[i],0):
        best = [x for x in fm.keys() if fm[x]==fm_max]
        gk = random.choice(best)    # if i want to move, leave it
        if g[i] != gk:
            g[i]=gk
        return True
    elif fm_max<0.0:  # escape: move into an empty cluster?
        gk=(set(range(len(g)))-set(g.values())).pop()
        g[i]=gk
        return True
    return False  # no movement for object i


def join(g:Dict[int,int], f:Callable[[int,int],float]) -> bool:
    """
    Join the most attractive clusters.

    Parameters
    ----------
    g : clustering of objects.
    f : function to calculate forces between objects.

    Returns
    -------
    bool Has changed something? If yes, then g has modified.
    """
    fs:Dict[Tuple[int,int],float] = {}
    for i in g:
        for j in g:         # take any pair of objects
            if g[i]!=g[j]:
                fs[(g[j],g[i])]=fs.get((g[j],g[i]),0.0)+f(i,j)
    fs_max=max(fs.values())
    if fs_max>0.0:  # merging is advantageous
        best = [x for x in fs.keys() if fs[x]==fs_max]
        if best:
            gj,gi = random.choice(best)  # select one of the best ones
            for k in g:
                if g[k]==gi:
                    g[k]=gj
            return True
    return False  # no merging
