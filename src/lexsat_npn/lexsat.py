from typing import Iterable

from pysat.formula import CNF
from pysat.solvers import Solver


def solve_lexsat(
        formula: CNF,
        variables: Iterable[int] = [],
        solver_name = "m22",
        verbose: bool = False
    ):
    """
    Inputs:
    - formula: CNF formula to be solved.
    - variables: list of interested variables, from most significant to least
        significant, to be in smallest lexicographic order. By default, it is
        all variables in the formula.
    - solver_name: name of the underlying SAT solver to use (default: "m22").
    - verbose: whether to print verbose information during solving.

    Outputs:
    - result: True if satisfiable, False otherwise.
    - model: assignment of interested variables if satisfiable, None otherwise.
    """
    if variables == []:
        variables = list(range(1, formula.nv + 1))

    result = []
    with Solver(name=solver_name) as s:
        s.append_formula(formula.clauses)

        # Initial satisfiability check
        if not s.solve():
            if verbose:
                print("[LEXSAT] UNSAT")
            return False, None

        # Iteratively find lexicographically smallest model
        model = s.get_model()
        if verbose:
            print("[LEXSAT] SAT")
            print("[LEXSAT] Initial model:", model)
        while True:
            # Accept False for the next variables
            # Flip the next variable assigned True
            for var in variables[len(result):]:
                result.append(-var)
                if var in model:
                    break
            if verbose:
                print("[LEXSAT] Current assumptions:", result)

            # Finish if all interested variables are decided
            if len(result) >= len(variables):
                break

            # If sat, update model and continue
            # If unsat, accept True for the last variable
            if s.solve(assumptions=result):
                model = s.get_model()
                if verbose:
                    print("[LEXSAT] New model:", model)
            else:
                result[-1] = -result[-1]
                if verbose:
                    print("[LEXSAT] Accept:", result[-1])

        if verbose:
            print("[LEXSAT] Final model:", result)
        return True, result


def solve_lexsat_max(
        formula: CNF,
        variables: Iterable[int] = [],
        solver_name = "m22",
        verbose: bool = False
    ):
    """
    Inputs:
    - formula: CNF formula to be solved.
    - variables: list of interested variables, from most significant to least
        significant, to be in largest lexicographic order. By default, it is
        all variables in the formula.
    - solver_name: name of the underlying SAT solver to use (default: "m22").
    - verbose: whether to print verbose information during solving.

    Outputs:
    - result: True if satisfiable, False otherwise.
    - model: assignment of interested variables if satisfiable, None otherwise.
    """
    if variables == []:
        variables = list(range(1, formula.nv + 1))

    result = []
    with Solver(name=solver_name) as s:
        s.append_formula(formula.clauses)

        # Initial satisfiability check
        if not s.solve():
            if verbose:
                print("[LEXSAT] UNSAT")
            return False, None

        # Iteratively find lexicographically smallest model
        model = s.get_model()
        if verbose:
            print("[LEXSAT] SAT")
            print("[LEXSAT] Initial model:", model)
        while True:
            # Accept True for the next variables
            # Flip the next variable assigned False
            for var in variables[len(result):]:
                result.append(var)
                if -var in model:
                    break
            if verbose:
                print("[LEXSAT] Current assumptions:", result)

            # Finish if all interested variables are decided
            if len(result) >= len(variables):
                break

            # If sat, update model and continue
            # If unsat, accept False for the last variable
            if s.solve(assumptions=result):
                model = s.get_model()
                if verbose:
                    print("[LEXSAT] New model:", model)
            else:
                result[-1] = -result[-1]
                if verbose:
                    print("[LEXSAT] Accept:", result[-1])

        if verbose:
            print("[LEXSAT] Final model:", result)
        return True, result
