from lexsat_npn import Formula, NPNTransformation, solve_lexsat


NUM_TRIAL = 10


if __name__ == "__main__":
    print("Loading AIG...")
    formula = Formula("examples/example_aig_4bit.aig")
    formula.build_cnf()
    truth_table = formula.truth_table()
    print("Input variables:", formula.input_variables)
    print("Output variable:", formula.output_variable)
    print("Original truth table:", truth_table)

    for i in range(NUM_TRIAL):
        print(f"\nApplying random NPN transformation (trial {i + 1}/{NUM_TRIAL})...")
        candidate = NPNTransformation.random(formula.num_bit)
        print("Candidate transformation:", candidate)

        lexsat_formula, lexsat_target = formula.build_lexsat(candidate)
        print("LEXSAT target:", lexsat_target)
        result, model, num_call = solve_lexsat(lexsat_formula, lexsat_target)
        print("Result:", result)
        print("Model:", model)
        print("Number of SAT calls:", num_call)

        if result is True:
            inputs = [i in model for i in lexsat_target]
            print("Input assignment:", inputs)
            original_output = formula.simulate(inputs)
            print("Original output:", original_output)
            improve = original_output is True

            formula.transformation = candidate
            candidate_output = formula.simulate(inputs)
            print("Candidate output:", candidate_output)
            print("Improvement:", improve)
            assert candidate_output ^ original_output

        new_truth_table = formula.truth_table()
        print("Transformed truth table:", new_truth_table)
        if result is False:
            assert new_truth_table == truth_table
        elif improve:
            assert new_truth_table < truth_table
        else:
            assert new_truth_table > truth_table
        truth_table = new_truth_table
