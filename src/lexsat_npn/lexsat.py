from typing import Iterable

from pysat.formula import CNF
from pysat.solvers import Solver


def solve_lexsat(
        formula: CNF,
        target: Iterable[int] = [],
        solver_name = "m22",
        verbose: bool = False
    ) -> tuple[bool, Iterable[int], int]:
    """
    Inputs:
    - formula: CNF formula to be solved.
    - target: targeted assignments, from most significant to least significant,
        to be achieved. By default, it is all the variables in the formula.
    - solver_name: name of the underlying SAT solver to use (default: "m22").
    - verbose: whether to print verbose information during solving.

    Outputs:
    - result: True if SAT, False otherwise.
    - model: assignment of variables if SAT, None otherwise.
    """
    if target == []:
        target = list(range(1, formula.nv + 1))
    else:
        for assignment in target:
            assert abs(assignment) <= formula.nv, "Target variable out of range."

    assumption, num_call = [], 1
    with Solver(name=solver_name) as s:
        s.append_formula(formula.clauses)

        # Initial satisfiability check
        if not s.solve():
            if verbose:
                print("[LEXSAT] UNSAT")
            return False, None, num_call

        # Iteratively try to achieve target assignments
        model = s.get_model()
        if verbose:
            print("[LEXSAT] SAT")
            print("[LEXSAT] Initial model:", model)
        while len(assumption) < len(target):
            # Accept the next variables if matching target
            # Flip the next variable not matching target
            for assignment in target[len(assumption):]:
                assumption.append(assignment)
                if assignment not in model:
                    if verbose:
                        print("[LEXSAT] Current assumptions:", assumption)

                    # Call SAT solver to check feasibility
                    num_call += 1
                    if s.solve(assumptions=assumption):
                        model = s.get_model()
                        if verbose:
                            print("[LEXSAT] New model:", model)
                    else:
                        assumption[-1] = -assumption[-1]
                        if verbose:
                            print("[LEXSAT] Accept:", assumption[-1])
                    break

        if verbose:
            print("[LEXSAT] Final model:", assumption)
        return True, model, num_call
