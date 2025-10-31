from .formula import TruthTable, Formula
from .lexsat import solve_lexsat


def flip_swap_lexsat_npn(formula: Formula) -> tuple[TruthTable, int, int]:
    num_bit = formula.num_bit
    num_trial = 0
    num_call = 0

    improvement = True
    while improvement:
        improvement = False

        # Try flipping the output and each input
        for i in range(num_bit + 1):
            candidate = formula.transformation.flip(i)
            lexsat_formula, lexsat_target = formula.build_lexsat(candidate)
            result, model, n_call = solve_lexsat(lexsat_formula, lexsat_target)
            num_trial += 1
            num_call += n_call
            if result is True:
                inputs = [i in model for i in lexsat_target]
                improve = formula.simulate(inputs)
                if improve:
                    formula.transformation = candidate
                    improvement = True

        # Try swapping each pair of inputs
        for i in range(num_bit - 1):
            for j in range(i + 1, num_bit):
                candidate = formula.transformation.swap(i, j)
                lexsat_formula, lexsat_target = formula.build_lexsat(candidate)
                result, model, n_call = solve_lexsat(lexsat_formula, lexsat_target)
                num_trial += 1
                num_call += n_call
                if result is True:
                    inputs = [i in model for i in lexsat_target]
                    improve = formula.simulate(inputs)
                    if improve:
                        formula.transformation = candidate
                        improvement = True

    best_truth_table = formula.truth_table()

    return best_truth_table, num_trial, num_call


def sifting_lexsat_npn(formula: Formula) -> tuple[TruthTable, int, int]:
    num_bit = formula.num_bit
    num_trial = 0
    num_call = 0

    improvement = True
    while improvement:
        improvement = False

        # Try sifting each input through all positions
        for i in range(1, num_bit):
            candidate = formula.transformation.copy()
            for j in range(1, 8 + 1):
                if j % 4 == 0:
                    # Swap input i with the next input
                    candidate = candidate.swap(i - 1, i)
                elif j % 2 == 0:
                    # Flip input i + 1
                    candidate = candidate.flip(i + 1)
                else:
                    # Flip input i
                    candidate = candidate.flip(i)

                lexsat_formula, lexsat_target = formula.build_lexsat(candidate)
                result, model, n_call = solve_lexsat(lexsat_formula, lexsat_target)
                num_trial += 1
                num_call += n_call
                if result is True:
                    inputs = [i in model for i in lexsat_target]
                    improve = formula.simulate(inputs)
                    if improve:
                        formula.transformation = candidate.copy()
                        improvement = True

    best_truth_table = formula.truth_table()

    return best_truth_table, num_trial, num_call