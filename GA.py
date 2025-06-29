# Implementacija genetskog algoritma

import random

# !!! This needs to be changer to work with permutations of multisets, and to add rotations crossover and chromosome instances !!!
def order_crossover(pairs):
    """
    Order Crossover (OX) implementation for genetic algorithms.
    It's used to make valid children from two parents when we work with permutations.
    """
    children = []
    for a, b in pairs:
        start = random.randint(0, len(a) - 1)
        end = random.randint(start + 1, len(a))

        child1 = [None] * len(a)
        child2 = [None] * len(b)

        child1[start:end] = a[start:end]
        child2[start:end] = b[start:end]

        fill_a = [x for x in b if x not in child1]
        fill_b = [x for x in a if x not in child2]

        index_a = 0
        index_b = 0

        for i in range(len(child1)):
            if child1[i] is None:
                child1[i] = fill_a[index_a]
                index_a += 1
            if child2[i] is None:
                child2[i] = fill_b[index_b]
                index_b += 1

        children.append(child1)
        children.append(child2)

    return children
    

if __name__ == '__main__':
    pass