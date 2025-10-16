from lexsat_npn import Formula, brute_force_npn, flip_swap_npn, sifting_npn


if __name__ == "__main__":
    print("Loading AIG...")
    formula = Formula("examples/example_aig_4bit.aig")
    print(formula.aig)

    print("\nSimulating truth table:")
    truth_table = formula.truth_table()
    print(truth_table)

    print("\nPerforming Brute Force NPN...")
    best_truth_table, num_trials = brute_force_npn(formula)
    print("Best Truth Table:", best_truth_table)
    print("Number of Trials:", num_trials)

    print("\nPerforming Flip and Swap NPN...")
    best_truth_table, num_trials = flip_swap_npn(formula)
    print("Best Truth Table:", best_truth_table)
    print("Number of Trials:", num_trials)

    print("\nPerforming Sifting NPN...")
    best_truth_table, num_trials = sifting_npn(formula)
    print("Best Truth Table:", best_truth_table)
    print("Number of Trials:", num_trials)
