from .formula import Formula, TruthTable
from .tt_npn import brute_force_tt_npn, flip_swap_tt_npn, sifting_tt_npn
from .lexsat_npn import flip_swap_lexsat_npn, sifting_lexsat_npn


def npn(formula: Formula, method: str) -> tuple[TruthTable, int, int]:
    if method == "brute_force_tt":
        best_truth_table, num_trial = brute_force_tt_npn(formula)
        num_call = 0
    elif method == "flip_swap_tt":
        best_truth_table, num_trial = flip_swap_tt_npn(formula)
        num_call = 0
    elif method == "sifting_tt":
        best_truth_table, num_trial = sifting_tt_npn(formula)
        num_call = 0
    elif method == "flip_swap_lexsat":
        num_trial, num_call = flip_swap_lexsat_npn(formula)
        best_truth_table = None
    elif method == "sifting_lexsat":
        num_trial, num_call = sifting_lexsat_npn(formula)
        best_truth_table = None
    else:
        raise ValueError(f"Unknown NPN method: {method}")

    return best_truth_table, num_trial, num_call
