from lexsat_npn import Formula, brute_force_tt_npn, flip_swap_tt_npn, sifting_tt_npn
from lexsat_npn import flip_swap_lexsat_npn, sifting_lexsat_npn


if __name__ == "__main__":
    print("Loading AIG...")
    formula = Formula("examples/example_aig_4bit.aig")
    print(formula.aig)

    print("\nSimulating truth table:")
    original_transformation = formula.transformation.random(formula.num_bit)
    print("Original Transformation:", original_transformation)
    formula.transformation = original_transformation.copy()
    truth_table = formula.truth_table()
    print(truth_table)


    print("\nPerforming Brute Force TT NPN...")
    formula.transformation = original_transformation.copy()
    best_truth_table, num_trial = brute_force_tt_npn(formula)
    print("Best Truth Table:", best_truth_table)
    print("Number of Trials:", num_trial)

    print("\nPerforming Flip and Swap TT NPN...")
    formula.transformation = original_transformation.copy()
    best_truth_table, num_trial = flip_swap_tt_npn(formula)
    print("Best Truth Table:", best_truth_table)
    print("Number of Trials:", num_trial)

    print("\nPerforming Sifting TT NPN...")
    formula.transformation = original_transformation.copy()
    best_truth_table, num_trial = sifting_tt_npn(formula)
    print("Best Truth Table:", best_truth_table)
    print("Number of Trials:", num_trial)

    formula.build_cnf()

    print("\nPerforming Flip and Swap LEXSAT NPN...")
    formula.transformation = original_transformation.copy()
    best_truth_table, num_trial, num_call = flip_swap_lexsat_npn(formula)
    print("Best Truth Table:", best_truth_table)
    print("Number of Trials:", num_trial)
    print("Number of SAT Calls:", num_call)

    print("\nPerforming Sifting LEXSAT NPN...")
    formula.transformation = original_transformation.copy()
    best_truth_table, num_trial, num_call = sifting_lexsat_npn(formula)
    print("Best Truth Table:", best_truth_table)
    print("Number of Trials:", num_trial)
    print("Number of SAT Calls:", num_call)
