# Implementation of Genetic Algorithm (GA)

import random
import numpy as np
from chromosome import Chromosome


def generate_individual(dimensions, paper_width, paper_height):
    """
    Generates a random individual (chromosome) based on the given dimensions.
    Args:
        dimensions (list[dict]): Dimensions of the shape numbers, each represented as a dictionary with 'width', 'height', and 'number' keys.
        paper_width (float): Width of the paper.
        paper_height (float): Height of the paper.
    """
    shape_order = []
    for idx, rect in enumerate(dimensions):
        shape_order.extend([idx] * rect["number"])

    random.shuffle(shape_order)

    rotations = [random.randint(0, 1) for _ in range(len(shape_order))]

    return Chromosome(shape_order, rotations, dimensions, paper_width, paper_height)


def generate_initial_chromosomes(pop_size, dimensions, paper_width, paper_height):
    """
    Generiše početnu populaciju sa datim brojem jedinki.
    
    :param pop_size: broj jedinki u populaciji
    :param dimensions: lista pravougaonika
    :return: lista jedinki (svaka jedinka je tuple: (shape_order, rotations))
    """
    return [generate_individual(dimensions, paper_width, paper_height) for _ in range(pop_size)]


def rank_chromosomes(chromosomes):
    """
    Ranks the chromosomes based on their fitness values.
    Args:   
        chromosomes (list[Chromosome]): List of chromosomes to be ranked.
    """
    return sorted(chromosomes, key=lambda x: x.fitness, reverse=True)


def natural_selection(chromosomes, n_keep):
    """
    Selects the first n chromosomes from the list.
    Args:
        chromosomes (list[Chromosome]): List of chromosomes to be selected from.
        n_keep (int): Number of chromosomes to keep based on fitness.
    """
    return chromosomes[:n_keep]


def elitis(chromosomes_old, chromosomes_new, elitis_rate, population_size):
    """
    Applies elitism to the population by selecting the best individuals from both old and new populations.
    Args:
        chromosomes_old (list[Chromosome]): List of old chromosomes.
        chromosomes_new (list[Chromosome]): List of new chromosomes.
        elitis_rate (float): Proportion of the population to be selected as elite.
        population_size (int): Total size of the population after elitism.
    """
    old_ind_size=int(np.round(population_size*elitis_rate))
    return chromosomes_old[:old_ind_size]+chromosomes_new[:(population_size-old_ind_size)]


def roulette_selection(parents):
    """
    Selects a pair of parents using roulette wheel selection based on their fitness values.
    Args:
        parents (list[Chromosome]): List of parent chromosomes.
    """
    pairs = []
    i = 0
    for i in range(0, len(parents), 2):
        weights=[]
        for i in range(len(parents)):
            weights.append((len(parents)-i)*random.random()) #za minimum
            #  weights.append((i+1)*random.random()) #za maksimum
        if (weights[0]>=weights[1]):
            maxInd1=0;
            maxInd2=1;
        else:
            maxInd1=1;
            maxInd2=0;

        for i in range(2,len(parents)):
            if weights[i]>weights[maxInd1]:
                maxInd2=maxInd1
                maxInd1=i
            elif weights[i]>weights[maxInd2]:
                maxInd2=1
        pairs.append([parents[maxInd1], parents[maxInd2]])
    return pairs


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

    
def mutate(chromosomes, mutation_rate, rotation_mutation_rate=0.1):
    """
    Mutates a list of chromosomes by swapping two random genes and changing the rotation of a gene with given mutation rates.
    Args:
        chromosomes (list[Chromosome]): List of chromosomes to mutate.
        mutation_rate (float): Probability of swapping two genes.
        rotation_mutation_rate (float): Probability of changing the rotation of a gene.
    """
    for chromosome in chromosomes:
        length = len(chromosome.shape_order)
        for i in range(length):
            # Change order of two figures
            if random.random() < mutation_rate:
                j = random.randint(0, length - 1)
                chromosome.shape_order[i], chromosome.shape_order[j] = chromosome.shape_order[j], chromosome.shape_order[i]
                chromosome.rotations[i], chromosome.rotations[j] = chromosome.rotations[j], chromosome.rotations[i]

            # Change rotation of a figure
            if random.random() < rotation_mutation_rate:
                chromosome.rotations[i] = not chromosome.rotations[i]


def genetic_algorithm(population_size, dimensions, paper_width, paper_height, generations=100, elitis_rate=0.1, mutation_rate=0.05, rotation_mutation_rate=0.1):
    """
    Runs the genetic algorithm for a given number of generations.
    Args:
        pop_size (int): Size of the population.
        dimensions (list[dict]): Dimensions of the shape numbers.
        paper_width (float): Width of the paper.
        paper_height (float): Height of the paper.
        generations (int): Number of generations to run the algorithm.
        elitis_rate (float): Proportion of the population to be selected as elite.
        mutation_rate (float): Probability of swapping two genes.
        rotation_mutation_rate (float): Probability of changing the rotation of a gene.
    """
    chromosomes = generate_initial_chromosomes(population_size, dimensions, paper_width, paper_height)

    for generation in range(generations):
        ranked_parents = rank_chromosomes(chromosomes)
        # parents = natural_selection(ranked_parents, population_size)
        pairs = roulette_selection(ranked_parents)
        children = order_crossover(pairs, dimensions, paper_width, paper_height)
        mutate(children, mutation_rate, rotation_mutation_rate)
        ranked_children = rank_chromosomes(children)
        chromosomes = elitis(ranked_parents, ranked_children, elitis_rate, population_size)

    best_chromosome = rank_chromosomes(chromosomes)[0]
    print(f"Best chromosome after {generations} generations: {best_chromosome}")
    best_chromosome.show(paper_width, paper_height, dimensions)



if __name__ == '__main__':
    # Example usage
    dimensions = [
        {"width": 100, "height": 50, "number": 2},
        {"width": 80, "height": 60, "number": 1},
        {"width": 40, "height": 30, "number": 3}
    ]
    paper_width = 500
    paper_height = 400
    population_size = 10

    genetic_algorithm(population_size, dimensions, paper_width, paper_height)