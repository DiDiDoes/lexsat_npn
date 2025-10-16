import copy
from itertools import product, permutations

from .formula import TruthTable, Formula
from .transformation import NPNTransformation

def brute_force_npn(formula: Formula) -> tuple[TruthTable, int]:
    num_bit = formula.num_bit
    best_truth_table = None
    num_trials = 0

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
                num_trials += 1
                if (best_truth_table is None) or (truth_table < best_truth_table):
                    best_truth_table = truth_table

    return best_truth_table, num_trials

def flip_swap_npn(formula: Formula) -> tuple[TruthTable, int]:
    num_bit = formula.num_bit
    best_truth_table = formula.truth_table()
    num_trials = 0

    improvement = True
    while improvement:
        improvement = False

        # Try flipping the output
        formula.transformation.output_negation = not formula.transformation.output_negation
        new_truth_table = formula.truth_table()
        num_trials += 1
        if new_truth_table < best_truth_table:
            best_truth_table = new_truth_table
            improvement = True
        else:
            formula.transformation.output_negation = not formula.transformation.output_negation

        # Try flipping each input
        for i in range(num_bit):
            formula.transformation.input_negation[i] = not formula.transformation.input_negation[i]
            new_truth_table = formula.truth_table()
            num_trials += 1
            if new_truth_table < best_truth_table:
                best_truth_table = new_truth_table
                improvement = True
            else:
                formula.transformation.input_negation[i] = not formula.transformation.input_negation[i]

        # Try swapping each pair of inputs
        for i in range(num_bit - 1):
            for j in range(i + 1, num_bit):
                formula.transformation.input_permutation[i], formula.transformation.input_permutation[j] = \
                    formula.transformation.input_permutation[j], formula.transformation.input_permutation[i]
                new_truth_table = formula.truth_table()
                num_trials += 1
                if new_truth_table < best_truth_table:
                    best_truth_table = new_truth_table
                    improvement = True
                else:
                    formula.transformation.input_permutation[i], formula.transformation.input_permutation[j] = \
                        formula.transformation.input_permutation[j], formula.transformation.input_permutation[i]

    return best_truth_table, num_trials

def sifting_npn(formula: Formula) -> tuple[TruthTable, int]:
    num_bit = formula.num_bit
    best_truth_table = formula.truth_table()
    num_trials = 0

    improvement = True
    while improvement:
        improvement = False
        best_transformation = copy.deepcopy(formula.transformation)

        # Try sifting each input through all positions
        for i in range(num_bit - 1):
            for j in range(8):
                if j % 4 == 0:
                    # Swap input i with the next input
                    formula.transformation.input_permutation[i], formula.transformation.input_permutation[i + 1] = \
                        formula.transformation.input_permutation[i + 1], formula.transformation.input_permutation[i]
                elif j % 2 == 0:
                    # Flip input i + 1
                    formula.transformation.input_negation[i + 1] = not formula.transformation.input_negation[i + 1]
                else:
                    # Flip input i
                    formula.transformation.input_negation[i] = not formula.transformation.input_negation[i]

                new_truth_table = formula.truth_table()
                num_trials += 1
                if new_truth_table < best_truth_table:
                    best_truth_table = new_truth_table
                    best_transformation = copy.deepcopy(formula.transformation)
                    improvement = True
            formula.transformation = copy.deepcopy(best_transformation)

    return best_truth_table, num_trials
