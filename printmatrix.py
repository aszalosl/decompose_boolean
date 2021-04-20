"""Print matrices and separators."""
from typing import List


def latex(solution1:List[List[int]],solution2:List[List[int]],matrix:List[List[int]]):
    """
    Reorder matrix based on solution.

    Parameters
    ----------
    solution1: clustering of rows as a list
    solution2: clustering of columns as a list
    matrix: matrix of the original relation

    Returns
    -------
    None. Just prints the matrix to the screen.
    """
    solr_len = [len(sublist) for sublist in solution1]
    stop=0
    stopr =  [stop:=stop+s for s in solr_len]
    flatr_list = [item-1 for group in solution1 for item in group]

    solc_len = [len(sublist) for sublist in solution2]
    stop=0
    stopc =  [stop:=stop+s for s in solc_len]
    flatc_list = [item-1 for group in solution2 for item in group]

    print("\\begin{tabular}{r|",end="")
    for j,y in enumerate(flatc_list):
        if j in stopc:
            print("|c",end="")
        else:
            print("c",end="")
    print("}\n  &",end="")

    for j,y in enumerate(flatc_list):
        if j<len(flatc_list)-1:
            print(f"{y+1}&",end="")
        else:
            print(f"{y+1}\\\\",end="")
    print(" \\hline",end="")

    for i,x in enumerate(flatr_list):
        if i in stopr:
            print(" \\hline")
        else:
            print()
        print(f"{x+1:2}", end="")
        for j,y in enumerate(flatc_list):
            print(f"&{matrix[x][y]}", end="")
        print("\\\\", end="")
    print(" \\hline\\end{tabular}")


def txt(solution1:List[List[int]],solution2:List[List[int]],matrix:List[List[int]]):
    """
    Reorder matrix based on solution.

    Parameters
    ----------
    solution1: clustering of rows as a list
    solution2: clustering of columns as a list
    matrix: matrix of the original relation

    Returns
    -------
    None. Just prints the matrix to the screen.
    """
    solr_len = [len(sublist) for sublist in solution1]
    stop=0
    stopr =  [stop:=stop+s for s in solr_len]
    flatr_list = [item-1 for group in solution1 for item in group]

    solc_len = [len(sublist) for sublist in solution2]
    stop=0
    stopc =  [stop:=stop+s for s in solc_len]
    flatc_list = [item-1 for group in solution2 for item in group]


    for i,x in enumerate(flatr_list):
        if i in stopr:
            print(" \n")
        else:
            print()
        print(f"{x+1:2}\t", end="")
        for j,y in enumerate(flatc_list):
            if j in stopc:
                print(" ", end="")
            print(f"{matrix[x][y]}", end="")
