import copy
from itertools import product, permutations

from .formula import TruthTable, Formula
from .transformation import NPNTransformation


def brute_force_tt_npn(formula: Formula) -> tuple[TruthTable, int]:
    num_bit = formula.num_bit
    best_truth_table = None
    num_trial = 0

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
                num_trial += 1
                if (best_truth_table is None) or (truth_table < best_truth_table):
                    best_truth_table = truth_table

    return best_truth_table, num_trial


def flip_swap_tt_npn(formula: Formula) -> tuple[TruthTable, int]:
    num_bit = formula.num_bit
    best_truth_table = formula.truth_table()
    num_trial = 0

    improvement = True
    while improvement:
        improvement = False

        # Try flipping the output and each input
        for i in range(num_bit + 1):
            candidate = formula.transformation.flip(i)
            new_truth_table = formula.try_transformation(candidate)
            num_trial += 1
            if new_truth_table < best_truth_table:
                best_truth_table = new_truth_table
                formula.transformation = candidate
                improvement = True

        # Try swapping each pair of inputs
        for i in range(num_bit - 1):
            for j in range(i + 1, num_bit):
                candidate = formula.transformation.swap(i, j)
                new_truth_table = formula.try_transformation(candidate)
                num_trial += 1
                if new_truth_table < best_truth_table:
                    best_truth_table = new_truth_table
                    formula.transformation = candidate
                    improvement = True

    return best_truth_table, num_trial


def sifting_tt_npn(formula: Formula) -> tuple[TruthTable, int]:
    num_bit = formula.num_bit
    best_truth_table = formula.truth_table()
    num_trial = 0

    improvement = True
    while improvement:
        improvement = False

        # Try sifting each input through all positions
        for i in range(1, num_bit):
            best_candidate = formula.transformation.copy()
            for j in range(1, 8 + 1):
                if j % 4 == 0:
                    # Swap input i with the next input
                    formula.transformation = formula.transformation.swap(i - 1, i)
                elif j % 2 == 0:
                    # Flip input i + 1
                    formula.transformation = formula.transformation.flip(i + 1)
                else:
                    # Flip input i
                    formula.transformation = formula.transformation.flip(i)

                new_truth_table = formula.truth_table()
                num_trial += 1
                if new_truth_table < best_truth_table:
                    best_truth_table = new_truth_table
                    improvement = True
                    best_candidate = formula.transformation.copy()
            formula.transformation = best_candidate.copy()

    return best_truth_table, num_trial
