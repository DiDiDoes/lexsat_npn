from itertools import product, permutations

from .formula import Formula
from .transformation import NPNTransformation


def brute_force_npn(formula: Formula):
    num_bit = formula.num_bit
    best_transformation = None
    best_truth_table = None

    for input_negation in product([False, True], repeat=num_bit):
        for input_permutation in permutations(range(num_bit)):
            for output_negation in [False, True]:
                transformation = NPNTransformation(
                    num_bit=num_bit,
                    input_negation=input_negation,
                    input_permutation=input_permutation,
                    output_negation=output_negation
                )
                formula.transformation = transformation
                truth_table = formula.truth_table()
                if (best_truth_table is None) or (truth_table < best_truth_table):
                    best_truth_table = truth_table
                    best_transformation = transformation

    return best_truth_table, best_transformation
