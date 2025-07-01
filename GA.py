# Implementation of Genetic Algorithm (GA)

import random
from chromosome import Chromosome


def order_crossover(pairs, dimensions, paper_width, paper_height):
    """
    Order Crossover (OX) implementation for genetic algorithms.
    It's used to make valid children from two parents when we work with permutations.
    Args:
        pairs (list[tuple[Chromosome, Chromosome]]): List of pairs of parent chromosomes.
        dimensions (list[dict]): Dimensions of the shape numbers.
        paper_width (float): Width of the paper.
        paper_height (float): Height of the paper.
    """
    children = []
    for a, b in pairs:
        start = random.randint(0, len(a) - 1)
        end = random.randint(start + 1, len(a))

        child1 = [None] * len(a)
        child2 = [None] * len(b)
        child1_rotations = [None] * len(a)
        child2_rotations = [None] * len(b)

        child1[start:end] = a.shape_order[start:end]
        child2[start:end] = b.shape_order[start:end]
        child1_rotations[start:end] = a.rotations[start:end]
        child2_rotations[start:end] = b.rotations[start:end]

        # this needs to be changed to work with multisets
        # fill_a = [x for x in b if x not in child1]
        # fill_b = [x for x in a if x not in child2]

        # shows the number of occurrences of each shape left to be filled in child1/child2
        dict_a = {}
        dict_b = {}
        for i in a.shape_order:
            if i not in dict_a:
                dict_a[i] = 0
                dict_b[i] = 0
            dict_a[i] += 1
            dict_b[i] += 1
        for i in a.shape_order[start:end]:
            dict_a[i] -= 1
        for i in b.shape_order[start:end]:
            dict_b[i] -= 1
        # fills child1 with remaining shapes from b
        fill_a = []
        fill_a_rotations = []
        for idx, val in enumerate(b.shape_order):
            if dict_a[val] > 0:
                fill_a.append(val)
                fill_a_rotations.append(b.rotations[idx])
                dict_a[val] -= 1
        # fills child2 with remaining shapes from a
        fill_b = []
        fill_b_rotations = []
        for idx, val in enumerate(a.shape_order):
            if dict_b[val] > 0:
                fill_b.append(val)
                fill_b_rotations.append(b.rotations[idx])
                dict_b[val] -= 1

        index_a = 0
        index_b = 0

        for i in range(len(child1)):
            if child1[i] is None:
                child1[i] = fill_a[index_a]
                child1_rotations[i] = fill_a_rotations[index_a]
                index_a += 1
            if child2[i] is None:
                child2[i] = fill_b[index_b]
                child2_rotations[i] = fill_b_rotations[index_b]
                index_b += 1

        children.append(Chromosome(child1, child1_rotations, dimensions, paper_width, paper_height))
        children.append(Chromosome(child2, child2_rotations, dimensions, paper_width, paper_height))

    return children
    

if __name__ == '__main__':
    pass