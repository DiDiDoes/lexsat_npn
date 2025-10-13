from lexsat_npn import Formula


if __name__ == "__main__":
    print("Loading AIG...")
    formula = Formula("examples/example_aig_4bit.aig")
    print(formula.aig)

    print("\nSimulating truth table:")
    truth_table = formula.truth_table()
    print(truth_table)

    print("\nBuilding CNF...")
    formula.build_cnf()
    cnf = formula.cnf
    print("CNF clauses:")
    for clause in cnf.clauses:
        print(clause)
    print("Number of variables:", cnf.nv)
    print("Inputs:", cnf.inps)
    print("Outputs:", cnf.outs)
