from lexsat_npn import Formula, brute_force_npn


if __name__ == "__main__":
    print("Loading AIG...")
    formula = Formula("examples/example_aig_4bit.aig")
    print(formula.aig)

    print("\nSimulating truth table:")
    truth_table = formula.truth_table()
    print(truth_table)

    print("\nPerforming Brute Force NPN...")
    best_truth_table, best_transformation = brute_force_npn(formula)
    print("Best Truth Table:", best_truth_table)
    print("Best Transformation:", best_transformation)
