# Author: Edvardas Scerbavicius
# E-mail: edvardas@gmail.com
# unit tests for these functions does'nt exists
"""Sort compare functions"""

def cmp_alpha(x, y):
    """alphabetic compare"""
    x0, y0 = x[0], y[0]
    if x0.upper() == y0.upper(): # A == a
        if (x0.isupper() and y0.isupper()) or (x0.islower() and y0.islower()): # A == A; a = a 
            return (x > y) and 1 or -1
        elif x0.isupper() and not y0.isupper(): # (A a) -> A < a
            return -1
        else: # (a A) -> a > A
            return 1

    elif x0.islower() and x0.upper() < y0.upper(): # (b C) -> b < c bet (d C) -> C > d !
        return -1

    elif y0.islower() and y0.upper() < x0.upper(): # (C b) -> C > b
        return 1

    else: # (a b), (B A)
        return (x > y) and 1 or -1


def cmp_simple(x, y):
    """return (x[1] > y[1]) and 1 or -1"""
    return (x[1] > y[1]) and 1 or -1
