# -*- coding: utf-8 -*-
from __future__ import print_function
import argparse
import codecs
from collections import defaultdict

"""
This file is part of the computer assignments for the course DD1418 at KTH.

This program computes the minimum-cost alignment of two strings.
"""

"""
When printing the results, only print BREAKOFF characters per line.
"""
BREAKOFF = 60


def compute_backpointers(s0, s1):
    """
    Computes and returns the backpointer table (see Jurafsky and Martin, 
    Fig. 2.21) arising from the calculation of the minimal edit distance 
    of two strings s0 and s1.

    The backpointer table has two dimensions: the row and column indices 
    of the table in Fig 2.21. The value are the coordinates of the cell
    the backpointer is pointing to. For example, if the backpointer from 
    cell (5,5) is to cell (5,4), then backptr[5][5] = (5,4).

    :param s0: The first string.
    :param s1: The second string.
    :return: The backpointer array.
    """
    
    if s0 == None or s1 == None:
        raise Exception('Both s0 and s1 has to be set')

    backptr = defaultdict(lambda:defaultdict(int))
    # key : value(of type int)
    

    m, n = len(s0), len(s1)
    dp = defaultdict(lambda: defaultdict(int))

    # Initialize base cases and backpointers for first row/column
    for i in range(0, m+1):
        dp[i][0] = i
        if i > 0:
            backptr[i][0] = (i-1, 0)
    for j in range(0, n+1):
        dp[0][j] = j
        if j > 0:
            backptr[0][j] = (0, j-1)

    # Fill DP matrix and record backpointers
    for i in range(1, m+1):
        for j in range(1, n+1):
            del_cost = dp[i-1][j] + 1
            ins_cost = dp[i][j-1] + 1
            sub_cost = dp[i-1][j-1] + subst_cost(s0[i-1], s1[j-1])

            best = min(del_cost, ins_cost, sub_cost)
            dp[i][j] = best

            # deterministically prefer substitution on ties, then deletion, then insertion
            if best == sub_cost:
                backptr[i][j] = (i-1, j-1)
            elif best == del_cost:
                backptr[i][j] = (i-1, j)
            else:
                backptr[i][j] = (i, j-1)
    
    # i-1, i, i+1
    
    #D(i,0) = i
    #D(0,k) = k
    #D
    
    #what is defaultdict? A dictionary that returns a default value when the key is not found.
    # In this case, it returns a defaultdict of int, which means that if a key is not found,
    # it will return 0 (the default value for int).
    
    
    # YOUR CODE HERE

    return backptr




def subst_cost(c0, c1):
    """
    The cost of a substitution is 2 if the characters are different
    or 0 otherwise (when, in fact, there is no substitution).
    """
    return 0 if c0 == c1 else 2



def align(s0, s1, backptr):
    """
    Finds the best alignment of two different strings s0 and s1 given
    a table of backpointers.

    The alignment is made by padding the input strings with spaces. If, 
    for instance, the strings are 'around' and 'rounded', then the 
    padded strings should be 'around  ' and ' rounded'.

    :param s0: The first string.
    :param s1: The second string.
    :param backptr: The backpointer table as returned by the 
    'compute_backpointes' function above.
    :return: A pair of (r1,r2), where r1 is s1 padded with spaces, as
    exemplified above, and r2 is s2 padded with spaces. 
    """

    r0,r1 = '',''

    # YOUR CODE HERE
    i, j = len(s0), len(s1)
    aligned0 = []
    aligned1 = []

    while not (i == 0 and j == 0):
        prev = backptr[i][j]
        if not isinstance(prev, tuple):
            # Defensive: if backpointer missing, stop
            break
        pi, pj = prev

        if pi == i-1 and pj == j-1:
            aligned0.append(s0[i-1])
            aligned1.append(s1[j-1])
        elif pi == i-1 and pj == j:
            aligned0.append(s0[i-1])
            aligned1.append(' ')
        else:  # pi == i and pj == j-1
            aligned0.append(' ')
            aligned1.append(s1[j-1])

        i, j = pi, pj

    r0 = ''.join(reversed(aligned0))
    r1 = ''.join(reversed(aligned1))

    return (r0,r1)




def print_alignment(s0,s1):
    """
    Prints two aligned strings (= strings padded with spaces).

    :param s0,s1: Two strings of equal length
    """
    assert len(s0) == len(s1)
    start_index = 0
    while start_index < len(s0):
        end_index = min(start_index+BREAKOFF, len(s0))
        print_list = ['', '', '']
        for i in range(start_index, end_index):
            print_list[0] += s0[i]
            print_list[1] += '|' if s0[i] == s1[i] else ' '
            print_list[2] += s1[i]

        for x in print_list:
            print(x)
        start_index += BREAKOFF


def main():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description='Aligner')
    # what does this do? It creates a parser object that can be used to parse command line arguments.
    group = parser.add_mutually_exclusive_group(required=True)
    # what does this do? It creates a group of arguments that are mutually exclusive, meaning that only one of them can be used at a time.
    group.add_argument('--file', '-f', type=str, nargs=2, help='align two strings')
    group.add_argument('--string', '-s', type=str, nargs=2, help='align the contents of two files')

    arguments = parser.parse_args()

    if arguments.file:
        f1, f2 = arguments.file
        with codecs.open(f1, 'r', 'utf-8') as f:
            s1 = f.read().replace('\r', '').replace('\n', ' ')
        with codecs.open(f2, 'r', 'utf-8') as f:
            s2 = f.read().replace('\r', '').replace('\n', ' ')

    elif arguments.string:
        s1, s2 = arguments.string
    
    padded1, padded2 = align(s1, s2, compute_backpointers(s1, s2))
    print_alignment( padded1, padded2 )

    
if __name__ == "__main__":
    main()