from pysat.formula import CNF

from lexsat_npn import solve_lexsat


if __name__ == "__main__":
    print("Testing LEXSAT solver on example satisfiable instance...")
    cnf = CNF(from_file="examples/example_sat.cnf")
    result, model = solve_lexsat(cnf, verbose=True)
    print("Result:", result)
    print("Model:", model)

    print("\nTesting LEXSAT solver on example unsatisfiable instance...")
    cnf = CNF(from_file="examples/example_unsat.cnf")
    result, model = solve_lexsat(cnf, verbose=True)
    print("Result:", result)
    print("Model:", model)
